'''
=================================================
Milestone 3

Nama  : Syahrul Budi Rahmadan
Batch : FTDS-002-SBY

This program was created to automate the transformation and load of data from PostgreSQL to ElasticSearch. The dataset used is a dataset regarding laptop sales.
=================================================
=================================================
By using important libraries such as:

1. Pandas for Viewing data and cleaning data
2. Psycopg2 for connection to Database
3. Numpy for mathematical calculations
4. Datetime to set the time
5. Airflow for DAG sets and operator functions
6. Elasticsearch for connection to elasticsearch and push to elasticsearch-kibana
=================================================
=================================================
Flow of this program can be seen as belowed:

1. Connect to postgres and check the connection
2. Query from postgres and save to local/server
3. Get data - Clean data - save to local/server with different name
4. Fetch data that has been cleaned to elasticsearch and then visualize it to kibana
=================================================
'''
import pandas as pd
import psycopg2 as db
import numpy as np

import datetime as dt
from datetime import timedelta

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from elasticsearch import Elasticsearch

def get_data():
    '''
    This function is used to fetch connections from posgresql/pgadmin 4 which will later store the dataset there
    
    By using the psycopg2 library, programmers can fetch Postgres databases easily without having to create additional, more complicated functions
    
    By entering the parameters as follows
    
    db_params = {
        'host': 'localhost', (Host yang ada di postgres)
        'database': 'xxxxx', (Nama database yang ingin diakses)
        'user': 'xxxx', (User ID)
        'password': 'xxxxx', (Password)
        'port': 'xxxxx', (Port yang akan dihubungkan ke Airflow (biasanya pada port yang tertulis ex: xxxxx:yyyy = y adalah portnya))
    }
    '''
    db_params = "dbname='airflow' host='postgres' user='airflow' password='airflow' port=5432"
    conn = db.connect(db_params) 
    
    df = pd.read_sql("select * from laptop_sales", conn)
    
    df.to_csv('/opt/airflow/dags/laptop_sales_from_posgres.csv', index=False)
    
def data_cleaning():
    '''
    This function is used for data cleaning, by utilizing the pandas library
    programmers do not need to create any more functions to perform data cleaning
    '''
    df_2 = pd.read_csv('/opt/airflow/dags/laptop_sales_from_posgres.csv', index_col=False)
    
    if df_2.duplicated().sum() > 0: df_2.drop_duplicates(inplace=True)
    
    if df_2.isnull().sum().sum() > 0: df_2.dropna(inplace=True)
    
    df_2.to_csv('/opt/airflow/dags/laptop_sales_from_posgres_cleaned.csv', index=True)
    
def posgretoElasticSearch():
    '''
    This function is used to push requests/uploads to Kibana via elastic search
    
    In this function the data will be checked whether the index (table) in Kibana already exists, if it does then it will
    the index is deleted.
    
    After that the data will be converted into .json using a function
    for i,r in df.iterrows():
        doc = r.to_json()
        res = es.index(index = "nama_index", body=doc)
    
    and the feed is pushed to the elastic-kibana server
    '''
    df = pd.read_csv('/opt/airflow/dags/laptop_sales_from_posgres_cleaned.csv', index_col=False)
    es = Elasticsearch('Elasticsearch')
    es.ping()
    
    es.delete_by_query(index="milestone_3_elastic_to_kibana", body={"query": {"match_all": {}}})

    for i,r in df.iterrows():
        doc = r.to_json()
        res = es.index(index = "milestone_3_elastic_to_kibana", body=doc)
    

# Fungsi ini dibuat untuk set otomasi pada Airflow        
default_args = {
    'owner': 'syahrul',
    'start_date': dt.datetime(2024, 1, 13, 6, 30, 0) - dt.timedelta(hours=7),
}


# Fungsi Dag
with DAG('Milestone_Dag_Every_630_morning', default_args = default_args,
            schedule_interval='30 6 * * *',  #30 6 * * *
            catchup=False
        ) as dag:
    '''
    In this DAG function, the functions that have been initiated previously (get_data, data_cleaning, and posgretoElasticSearch)
    will be entered into a process which is usually called a DAG
    
    In this process, automation is also initiated from the default arguments that were created previously
    '''
    # Task 1 fetch postgres
    Fetchfromposgres = PythonOperator(task_id='Fetchfromposgres', python_callable=get_data)
    
    # Task 2 cleaning data
    cleaningdata = PythonOperator(task_id='cleaningdata', python_callable=data_cleaning)
    
    # Task 3 push to elastic-kibana
    pushtoelastic = PythonOperator(task_id='pushtoelastic', python_callable=posgretoElasticSearch)

# The process will start from Fetchfromposgres -> cleaningdata -> pushtoelastic
Fetchfromposgres >> cleaningdata >> pushtoelastic