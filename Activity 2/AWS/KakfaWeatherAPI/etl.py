from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import requests
import psycopg2
import os
from config import api_key

def get_weather(api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": 40.806862,
        "lon": -96.681679,
        "appid": api_key,
        "units": "metric"  # For temperature in Celsius
    }

    response = requests.get(base_url, params=params)
    data = response.json()
    temperature = data['main']['temp']
    timestamp = datetime.now().replace(minute=0, second=0, microsecond=0)

    # Connect to Amazon RDS
    conn = psycopg2.connect(
        host=os.environ.get('RDS_HOST'),
        database=os.environ.get('RDS_DB_NAME'),
        user=os.environ.get('RDS_USERNAME'),
        password=os.environ.get('RDS_PASSWORD')
    )

    # Insert data into RDS
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO weather_data (temperature, timestamp) VALUES (%s, %s)",
            (temperature, timestamp)
        )
    conn.commit()
    conn.close()

# Set up default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 10, 7),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Create the DAG
dag = DAG(
    'openweather_to_rds',
    default_args=default_args,
    description='Fetch hourly temperature from OpenWeather and send to Amazon RDS',
    schedule_interval='@hourly',
)

# Define the task
fetch_temperature_task = PythonOperator(
    task_id='fetch_and_store_temperature',
    python_callable=get_weather,
    dag=dag,
)

# Set up task dependencies
fetch_temperature_task