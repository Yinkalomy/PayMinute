# Data Warehouse Development for Pay Minute


## Introduction
- PayMinute is a Fintech Company with over
5000 active users located in Nigeria and
Kenya; 
- They currently have Data Analysts whose
daily tasks is to deliver analysed data to
the department heads and board members
weekly; 
- The analysts have since began to experience
delayed data retrieval and need for
multiple-checks on data accuracy as their
daily transactions grew;
- the goal of the project is to develop a high performing data warehouse architecture for the Data analytists.

## Description of Project
- The database of the company was stored in the Postgresql and subsequently extracted using Pandas to a datalake (Amazon S3 bucket);
- the data is moved from the staging area to the core area (Amazon Redshift) where it exists as a snowflake schema model;
- The Data is transformed to star schemas to ensure ease of data retrieval

## Tools installed for the project
- boto3==1.28.48
- botocore==1.31.48
- fsspec==2023.9.0
- jmespath==1.0.1
- numpy==1.25.2
- pandas==2.1.0
- psycopg2==2.9.7
- python-dateutil==2.8.2
- pytz==2023.3.post1
- s3fs==0.4.2
- s3transfer==0.6.2
- six==1.16.0
- tzdata==2023.3
- urllib3==1.26.16

## File Structure
- the source code is the index.py file where the series of codes of executed in the python script;
- codes required to establish connection to amazon S3 and Redshift are found in helpers.py and table variables are defined in constant.py. Both files are stored in the utils folder;
- the sql statements are found in the sql_statement folder that houses the create.py and transform.py files;
- the following steps were followed:

## steps in the source code
- Created a bucket using boto3
- Extracted from the database (postgresql) to the Data Lake (S3)
- Created the Raw Schema in the Data Warehouse
- Created the raw (development) schema and created the raw table
- Copied the table from the S3 bucket to Amazon Redshift
- Created the fact and dimension tables in a star schema
- inserted data into the model
- Performed Data Quality check

## Conclusion
- Project ran successfully
