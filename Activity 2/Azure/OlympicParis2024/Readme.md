
# Overview: Azure data engineering project for Olympic Paris 2024 dataset 

**Goal: The goal of this project is to demonstrate using tools on Microsoft Azure portal to build end-to-end data pipeline. The process is shown in the image below.**

![](image/Azure.png)

We use a variety of tools on Microsoft Azure for this project. The process started from using **Azure Data Factory** to ingest raw data from the source. After the data ingestion, the raw data is stored in the **Azure Data Lake Gen2**. Then, we use **Azure Databricks** to perform data cleaning and data transformation. We will store the clean data into the **Azure Data Lake Gen2**. After that, we connect the **Azure Data Lake Gen2** with the **Azure Synapse Analytics** to perform analytics. Finally, we will use **PowerBI** for dashboard and reporting.


