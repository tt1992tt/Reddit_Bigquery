from google.cloud import bigquery

def load_bigquery():
    
    client = bigquery.Client()
    table_id = 'fifth-brook-368722.reddit.reddit_trends'
    
    job_config = bigquery.LoadJobConfig(
          schema = [
            bigquery.SchemaField("TITLE", "STRING"),
            bigquery.SchemaField("DATE", "DATE"),
            bigquery.SchemaField("LINK", "STRING"),
            bigquery.SchemaField("NUM_COMMENTS", "INTEGER"),
            bigquery.SchemaField("NUM_REPORTS", "INTEGER"),
            bigquery.SchemaField("SCORE", "INTEGER")
          ],
          skip_leading_rows=1, # salto las cabeceras
          source_format = bigquery.SourceFormat.CSV,
      )   
      
    uri = 'gs://bucket_tt/upload_test/test.csv' # ruta fisica del archivo en la nube
    load_job = client.load_table_from_uri(uri, table_id, job_config=job_config) # api request
    load_job.result() # espero que se complete el job
    destination_table = client.get_table(table_id)