# Stock Price Prediction ETL Project

**Overview:** The purpose of this project is to perform stock price prediction of next 5 days using the previous stock price. The Airflow is set up using the EC2 instance and the historical and prediction data is stored in PostgresSQL database using Amazon RDS. The historical and the prediction stock price can be visualized on my personal website.

</br>

**Keyword:** Airflow, Prophet, AWS (EC2, S3, RDS)

</br>

**API Link:** https://developers.google.com/youtube/v3/getting-started
* This project uses the Youtube comments api in the link.

</br>

**Model Link:** https://facebook.github.io/prophet/

</br>

**Project File Links:**
- <a href="dag.py">dag.py</a>

</br>

**Project Mapflow:**
![](process.png)

</br>

**Steps:**
1. Set up Amazon RDS (PostgresSQL Database)
2. Create EC2 instance (ubuntu) and set up airflow in the instance. Also, set up PostgreSQL in the instance.  
3. Set up dag.py to configure the DAG on Airflow.
4. Run the pipeline.

</br>

### Step 1. Set up Amazon RDS (PostgresSQL Database)
In this step, we will set up the Amazon RDS database to store data.



### Step 2. Create EC2 instance 
In this step, we will create an EC2 instance and set up airflow in the instance. Also, set up PostgreSQL in the instance.  



