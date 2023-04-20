### Overview
**Goal:** The purpose of this documentation is to explain the Machine Learning Workflow on cloud using AWS.


### Section 1: Machine Learning Workflow

**1) Ingest & Analyze**: Data Exploration, Bias Detection

- Amazon S3 & Amazon Athena
- AWS Glue
- Amazon SageMaker Data Wrangler & Clarify

**2) Prepare & Transform**: Feature Engineering, Feature Store

- Amazon SageMaker Data Wrangler
- Amazon SageMaker Processing Jobs
- Amazon SageMaker Feature Store

**3) Train & Tune**: Automated ML, Model train and tune

- Amazon SageMaker Autopilot
- Amazon SageMaker Training & Debugger
- Amazon SageMaker Hyperparameter Tuning

**4) Deploy & Manage**: Model Deployment, Automated Pipelines

- Amazon SageMaker Endpoints
- Amazon SageMaker Batch Transform
- Amazon SageMaker Pipelines

### Section 2: AWS Components

**1) Amazon S3:** 
- Amazon Simple Storage Service
- Object storage
- Durable, available, exabyte scale
- Secure, compliant, auditable

**2) AWS Data Wrangler:**
- Open source Python library
- Connects pandas DataFrames and AWS data services
- Load/unload data from: (1) Data lakes, (2) Data warehouses, (3) Database
- Code Example: 

!pip install awswrangler

import awswrangler as wr
import pandas as pd

df = wr.s3.read_csv(path='s3//bucket/prefix/')
