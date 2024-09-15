
# Overview: Azure data engineering project for Olympic Paris 2024 dataset 

**Goal:** The goal of this project is to demonstrate using tools on Microsoft Azure portal to build end-to-end data pipeline. The process is shown in the image below.

![](image/Azure.png)

We use a variety of tools on Microsoft Azure for this project. The process started from using **Azure Data Factory** to ingest raw data from the source. After the data ingestion, the raw data is stored in the **Azure Data Lake Gen2**. Then, we use **Azure Databricks** to perform data cleaning and data transformation. We will store the clean data into the **Azure Data Lake Gen2**. After that, we connect the **Azure Data Lake Gen2** with the **Azure Synapse Analytics** to perform SQL-based analytics. Finally, we will use **PowerBI** for dashboard and reporting.


## 1. Azure Data Factory

![](image/Azure_Data_Factory_Activities.png)

In this part, we use Azure Data Factory to ingest data from the source. We create multiple copy activites in the pipeline to copy data from the source to sink (Azure Data Lake Stirage Gen2). 

## 2. Azure Data Lake Storage Gen2

We set up a raw and a transformed folders in the container. The raw folder is used to store the raw data, while the transformed folder is used to store the cleaned data.

![](image/Azure_Data_Lake_Storage_Gen2_Container.png)

The files in the raw data folder is shown below:

![](image/Azure_Data_Lake_Storage_Gen2_Raw.png)


## 2. Azure Databricks

In this part, we load the raw data into Azure databricks environment and perform data cleaning and data transformation.
