import psycopg2
import pandas as pd
from sqlalchemy import create_engine
import boto3
from utils.helper import create_bucket, connect_to_dwh
from configparser import ConfigParser
from utils.constants import db_tables
from sql_statements.create import raw_data_tables, transformed_tables
from sql_statements.transform import transformation_queries
import redshift_connector

config = ConfigParser()
config.read('.env')

region = config['AWS']['region']
bucket_name= config['AWS']['bucket_name']
access_key = config['AWS']['access_key']
secret_key = config['AWS']['secret_key']

host = config['DB_CRED']['host']
user = config['DB_CRED']['username']
password = config['DB_CRED']['password']
database = config['DB_CRED']['database']

dwh_host = config['DWH']['host']
dwh_user = config['DWH']['username']
dwh_password = config['DWH']['password']
dwh_database = config['DWH']['database']
role = config['DWH']['role']

# --- step 1: Create a bucket using boto3

create_bucket(access_key, secret_key, bucket_name)

# --- step 2: Extract from Database to Data Lake (S3)

conn = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:5432/{database}')

df = pd.read_sql_query('SELECT * FROM {table_name}', conn)

s3_path = 's3://{}/{}.csv'

for table in db_tables:
    query = f'SELECT * FROM {table}'
    df = pd.read_sql_query(query, conn)

    df.to_csv(
        s3_path.format(bucket_name, table), 
        index=False,
        storage_options={
            'key': access_key,
            'secret': secret_key
        }
    )

# --- step 3: Create the Raw Schema in DWH
conn_details = {
    'host' : dwh_host,
    'user': dwh_user,
    'password' : dwh_password,
    'database' : dwh_database
}
dwh_conn = connect_to_dwh(conn_details)

schema = 'raw_data'
staging_schema = 'staging_data'

print('conn successful')

cursor = dwh_conn.cursor()
# --- Create the raw(development) Schema

create_dev_schema_query = 'CREATE SCHEMA IF NOT EXISTS raw_data;'
cursor.execute(create_dev_schema_query)

# --- Creating the raw tables
for query in raw_data_tables:
    print(f'========{query[:50]}')
    cursor.execute(query)
    dwh_conn.commit()

# --- copy from s3 to Redshift

for table in db_tables:
    query = f'''
        copy {schema}.{table} 
        from '{s3_path.format(bucket_name, table)}'
        iam_role '{role}'
        delimiter ','
        ignoreheader 1;'''
    
    cursor.execute(query)
    dwh_conn.commit()

 # --- step 4: Create fact and dimensions

# --- create schema
create_staging_schema_query = 'CREATE SCHEMA IF NOT EXISTS staging_data;'
cursor.execute(create_staging_schema_query)
dwh_conn.commit()

# --- create star schema tables (fact and dims)
for query in transformed_tables:
     print(f'========{query[:50]}')
     cursor.execute(query)
     dwh_conn.commit()

#---- insert the data into the facts and dimensions

for query in transformation_queries:
    print(f'========{query[:50]}')
    cursor.execute(query)
    dwh_conn.commit()

#--- step 5: Data Quality check
staging_tables = ['ft_customer_transactions', 'dim_wallets', 'dim_dates', 'dim_customers', 'dim_banks']
query = 'SELECT COUNT(*) FROM staging_data.{}'

for table in staging_tables:
    cursor.execute(query.format(table))
    print(f'Table {table} has {cursor.fetchall()} rows')



cursor.close()
dwh_conn.close()