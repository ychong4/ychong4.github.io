from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import requests
import pandas as pd
import psycopg2
from psycopg2 import sql
import requests
from datetime import datetime
from prophet import Prophet
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from datetime import datetime
import boto3
import json

api_key = <-------API Key-------------->

def get_secret():

    secret_name = "<-------Secret Name-------------->
    region_name = "us-east-2"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    get_secret_value_response = client.get_secret_value(
        SecretId=secret_name
    )

    response = get_secret_value_response['SecretString']
    secret = json.loads(response)
    return secret['username'], secret['password']

username, password = get_secret()

db_params = {
        'user': username,
        'password': password,
        'host': 'db-stock.cbueaqgy4mwk.us-east-2.rds.amazonaws.com',
    }
tickers = ['AAPL', 'NVDA', 'META', 'MSFT', 'AMZN']

# Get today's date in the required format
today = pd.Timestamp.now(tz='UTC').normalize().strftime('%Y-%m-%d')

# Default arguments for DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 10, 20, 15, 0),  # Adjust start date
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}



def fetch_stock_data(**context):
    # Initialize an empty list to store DataFrames
    dataframes = []

    # Get today's date in YYYY-MM-DD format
    today = datetime.today().strftime('%Y-%m-%d')
    
    # Set the start_date and end_date to today
    start_date = today
    end_date = today

    # Loop over each ticker to fetch the daily time series data
    for ticker in tickers:
        # Construct the API URL
        url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{start_date}/{end_date}?apiKey={api_key}"
        
        # Make the API request
        response = requests.get(url)
        
        # Check if the response is successful
        if response.status_code == 200:
            data = response.json()
            
            # Extract the results if they exist
            if 'results' in data and data['results']:
                # Create a DataFrame from the data
                df = pd.DataFrame(data['results'])
                
                # Rename the columns for clarity
                df.rename(columns={
                    't': 'date',
                    'o': 'open',
                    'h': 'high',
                    'l': 'low',
                    'c': 'close',
                    'v': 'volume'
                }, inplace=True)
                
                # Convert timestamp to datetime and format
                df['date'] = pd.to_datetime(df['date'], unit='ms').dt.date
                df = df.drop(columns=['vw', 'n'])

                # Add the ticker column
                df['ticker'] = ticker
                
                # Append the DataFrame to the list
                dataframes.append(df)
            else:
                print(f"No data available for {ticker} on {start_date}.")
        else:
            print(f"Failed to fetch data for {ticker}: {response.text}")

    # Combine all DataFrames into one
    if dataframes:
       
        final_df = pd.concat(dataframes, ignore_index=True)
         # Push the DataFrame into XCom
        context['ti'].xcom_push(key='final_df', value=final_df.to_dict())
        print("Final DataFrame for today:")
        print(final_df)

        return final_df
    else:
        print("No data available for today.")
        return None


def insert_daily_stock_data_to_db(**context):
    final_df_data = context['ti'].xcom_pull(key='final_df')
    final_df = pd.DataFrame(final_df_data)
    print(final_df)

    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()
    
        # Insert DataFrame into PostgreSQL table
        insert_query = sql.SQL("""
            INSERT INTO stock_historical_price (date, close, volume, open, high, low, ticker)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """)
        # Iterate over DataFrame rows and execute the insert statement


        for index, row in final_df.iterrows():
            cursor.execute(insert_query, (row['date'], row['close'], row['volume'], row['open'], row['high'], row['low'], row['ticker']))
    
        # Commit the changes
        conn.commit()
        print("Data inserted into database")

    except Exception as error:
        print(f"Error occured: {error}")
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    
def read_historical_stock_data_from_db_and_make_prediction(**context):

    # Establish the connection to the PostgreSQL database
    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()
        
        # Insert data into the stock_prediction_price table
        select_query = """
            SELECT * FROM stock_historical_price;
        """
    
        cursor.execute(select_query)
        # Fetch all rows from the executed query
        rows = cursor.fetchall()
    
        column_names = [desc[0] for desc in cursor.description]
    
        # Create a DataFrame using the fetched data and column names
        df = pd.DataFrame(rows, columns=column_names)
        print(df.head())
    
    except Exception as e:
        print(f"An error occurred: {e}")
        
    finally:
        # Close the database connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            print("PostgreSQL connection closed.")

    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by='date')
    
    def compute_indicators(df):
        # Calculate 5-day and 20-day moving averages
        df['sma_5'] = df['close'].rolling(window=5).mean()
        df['sma_20'] = df['close'].rolling(window=20).mean()
        
    
        # Calculate RSI (Relative Strength Index)
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))
    
        # Create Lag Features for the past 5 days for all variables
        for i in range(1, 6):  # Create lag features for the past 5 days (1 to 5)
            df[f'close_lag_{i}'] = df['close'].shift(i)
            df[f'volume_lag_{i}'] = df['volume'].shift(i)
            df[f'open_lag_{i}'] = df['open'].shift(i)
            df[f'high_lag_{i}'] = df['high'].shift(i)
            df[f'low_lag_{i}'] = df['low'].shift(i)
            df[f'sma_5_lag_{i}'] = df['sma_5'].shift(i)
            df[f'sma_20_lag_{i}'] = df['sma_20'].shift(i)
            df[f'rsi_lag_{i}'] = df['rsi'].shift(i)
    
        # Drop rows with NaN values
        df.dropna(inplace=True)
    
        # Reset index
        df.reset_index(drop=True, inplace=True)
    
        return df
    
    tickers = ['AAPL', 'NVDA', 'META', 'MSFT', 'AMZN']
    
    # Create a dictionary to hold DataFrames for each ticker
    ticker_dfs = {ticker: df[df['ticker'] == ticker].reset_index(drop=True) for ticker in tickers}
    
    # Access individual DataFrames
    df_aapl = ticker_dfs['AAPL']
    df_nvda = ticker_dfs['NVDA']
    df_meta = ticker_dfs['META']
    df_msft = ticker_dfs['MSFT']
    df_amzn = ticker_dfs['AMZN']
    
    # Apply to each ticker DataFrame
    for ticker in tickers:
        ticker_dfs[ticker] = compute_indicators(ticker_dfs[ticker])
    
    all_predictions =[]
    
    for ticker in tickers:
        ticker_dfs[ticker].rename(columns={'date': 'ds', 'close': 'y'}, inplace=True)
        
        # Select features including 5-day lag features for volume, open, high, low, and other indicators
        df_prophet = ticker_dfs[ticker][['ds', 'y', 
                                         'volume_lag_1', 'volume_lag_2', 'volume_lag_3', 'volume_lag_4', 'volume_lag_5',
                                         'open_lag_1', 'open_lag_2', 'open_lag_3', 'open_lag_4', 'open_lag_5',
                                         'high_lag_1', 'high_lag_2', 'high_lag_3', 'high_lag_4', 'high_lag_5',
                                         'low_lag_1', 'low_lag_2', 'low_lag_3', 'low_lag_4', 'low_lag_5',
                                         'sma_5_lag_1', 'sma_20_lag_1', 'rsi_lag_1']]
        
        # Apply StandardScaler to the training data (for regressor variables only)
        scaler = StandardScaler()
        
        regressor_cols = ['volume_lag_1', 'volume_lag_2', 'volume_lag_3', 'volume_lag_4', 'volume_lag_5',
                          'open_lag_1', 'open_lag_2', 'open_lag_3', 'open_lag_4', 'open_lag_5',
                          'high_lag_1', 'high_lag_2', 'high_lag_3', 'high_lag_4', 'high_lag_5',
                          'low_lag_1', 'low_lag_2', 'low_lag_3', 'low_lag_4', 'low_lag_5',
                          'sma_5_lag_1', 'sma_20_lag_1', 'rsi_lag_1']
    
        # Fit scaler on regressors
        df_prophet_scaled = df_prophet.copy()
        df_prophet_scaled[regressor_cols] = scaler.fit_transform(df_prophet[regressor_cols])
        
        # Initialize and configure Prophet model with scaled regressors
        model = Prophet()
        for regressor in regressor_cols:
            model.add_regressor(regressor)
    
        # Fit the model
        model.fit(df_prophet_scaled)
    
        # Make recursive predictions for next 5 business days
        last_known_data = df_prophet.iloc[-1].copy()  # Get last known values for lag features
    
        # Create future date (i.e., next business day)
        future_dates = model.make_future_dataframe(periods=5, freq='B')
    
        # Filter to keep only future dates
        future_dates = future_dates[future_dates['ds'] > df_prophet['ds'].max()]
    
            
        for future_date in future_dates['ds']:
            # Populate lagged values based on the last known data
            future_data = {
                'ds': future_date,
                'volume_lag_1': last_known_data['volume_lag_1'],
                'volume_lag_2': last_known_data['volume_lag_2'],
                'volume_lag_3': last_known_data['volume_lag_3'],
                'volume_lag_4': last_known_data['volume_lag_4'],
                'volume_lag_5': last_known_data['volume_lag_5'],
                'open_lag_1': last_known_data['open_lag_1'],
                'open_lag_2': last_known_data['open_lag_2'],
                'open_lag_3': last_known_data['open_lag_3'],
                'open_lag_4': last_known_data['open_lag_4'],
                'open_lag_5': last_known_data['open_lag_5'],
                'high_lag_1': last_known_data['high_lag_1'],
                'high_lag_2': last_known_data['high_lag_2'],
                'high_lag_3': last_known_data['high_lag_3'],
                'high_lag_4': last_known_data['high_lag_4'],
                'high_lag_5': last_known_data['high_lag_5'],
                'low_lag_1': last_known_data['low_lag_1'],
                'low_lag_2': last_known_data['low_lag_2'],
                'low_lag_3': last_known_data['low_lag_3'],
                'low_lag_4': last_known_data['low_lag_4'],
                'low_lag_5': last_known_data['low_lag_5'],
                'sma_5_lag_1': last_known_data['sma_5_lag_1'],
                'sma_20_lag_1': last_known_data['sma_20_lag_1'],
                'rsi_lag_1': last_known_data['rsi_lag_1']
            }
            
            # Scale the input data
            future_df = pd.DataFrame([future_data])
            future_df[regressor_cols] = scaler.transform(future_df[regressor_cols])
            
            # Make prediction
            forecast = model.predict(future_df)
            predicted_price = forecast['yhat'].values[0]
            predicted_price_upper = forecast['yhat_upper'].values[0]
            predicted_price_lower = forecast['yhat_lower'].values[0]
            
            all_predictions.append({
                'ticker': ticker,
                'insert_date': (pd.Timestamp.today() - pd.Timedelta(days=1)).date(),
                'prediction_date': future_date,
                'price': predicted_price,
                'price_upper': predicted_price_upper,
                'price_lower': predicted_price_lower
            })
    
    # Create a DataFrame from the predictions
    prediction_df = pd.DataFrame(all_predictions)
    print(prediction_df)

    # Push the DataFrame into XCom
    context['ti'].xcom_push(key='prediction_df', value=prediction_df)

def insert_daily_prediction_data_to_db(**context):

    prediction_df = context['ti'].xcom_pull(key='prediction_df')
    print(prediction_df)
    # Establish the connection to the PostgreSQL database
    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()
        
        # Insert data into the stock_prediction_price table
        insert_query = """
            INSERT INTO stock_prediction_price (ticker, insert_date, prediction_date, price, price_upper, price_lower)
            VALUES (%s, %s, %s, %s, %s, %s);
        """
    
        for index, row in prediction_df.iterrows():
            cursor.execute(insert_query, (row['ticker'], row['insert_date'], row['prediction_date'], row['price'], row['price_upper'], row['price_lower']))
    
        # Commit the transaction
        conn.commit()
        print("Data inserted successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Close the database connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            print("PostgreSQL connection closed.")

# Define the DAG
with DAG(
    'stock_data_prediction_pipeline',
    default_args=default_args,
    description='DAG to fetch stock data, compute for prediction, and insert into database',
    schedule_interval='0 15 * * 1-5',  # Run Monday to Friday at 10 PM
    catchup=False
) as dag:

    # Task 1: Fetch stock data from API
    fetch_stock_data_task = PythonOperator(
        task_id='fetch_stock_data',
        python_callable=fetch_stock_data,
        provide_context=True
    )
    
    # Task 2: Insert stock data into the database
    insert_daily_stock_data_task = PythonOperator(
        task_id='insert_stock_data_to_db',
        python_callable=insert_daily_stock_data_to_db,
        provide_context=True
    )

    # Task 3: Read all historical stock data from the database
    read_historical_stock_data_from_db_and_make_prediction_task = PythonOperator(
        task_id='read_all_historical_stock_data_from_db',
        python_callable=read_historical_stock_data_from_db_and_make_prediction,
        provide_context=True
    )

    # Task 4: Insert prediction data into the database
    insert_daily_prediction_data_task = PythonOperator(
        task_id='insert_daily_prediction_data_to_db',
        python_callable=insert_daily_prediction_data_to_db,
        provide_context=True
    )

    # Set task dependencies
    fetch_stock_data_task >> insert_daily_stock_data_task >> read_historical_stock_data_from_db_and_make_prediction_task >> insert_daily_prediction_data_task
