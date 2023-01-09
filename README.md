# Reddit_Bigquery

Fetch the most hot topics on /r/argentina from Reddit, via OAuth2 authorization. 
Load the data into Google Cloud Storage in .csv format
Transfer the .csv file from Cloud Storage to BigQuery

Create table in BigQuery with incoming .csv data structure

Setup Airflow2 environment (Cloud Composer) and create a DAG to orchestrate the entire process.

Reddit -> Cloud Storage -> BigQuery
