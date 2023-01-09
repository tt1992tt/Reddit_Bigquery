# Reddit_Bigquery

Fetch the most hot topics on /r/argentina from Reddit, via OAuth2 authorization.<br /> 
Load the data into Google Cloud Storage in .csv format<br />
Transfer the .csv file from Cloud Storage to BigQuery<br />

Create table in BigQuery with incoming .csv data structure<br />

Create serverless Airflow environment (Cloud Composer) and configure a DAG to orchestrate the entire process.

Reddit -> Cloud Storage -> BigQuery
