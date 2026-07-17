from dotenv import load_dotenv
import os
import logging
import pandas as pd
from google.cloud import bigquery
from google.cloud.exceptions import NotFound

load_dotenv()

logger = logging.getLogger(__name__)

project_id = os.getenv("PROJECT_ID")
dataset_id = os.getenv("DATASET_ID")
table_id = f"{project_id}.{dataset_id}.staging_jobs"
google_app_credentials = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

if not project_id:
    raise EnvironmentError("Project ID not configured")

if not dataset_id:
    raise EnvironmentError("Dataset ID not configured")

if not google_app_credentials:
    raise EnvironmentError("Google App Credentials are missing or not configured")

schema = [
    bigquery.SchemaField("job_id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("title", "STRING"),
    bigquery.SchemaField("job_type", "STRING"),
    bigquery.SchemaField("company", "STRING"),
    bigquery.SchemaField("location", "STRING"),
    bigquery.SchemaField("country", "STRING"),
    bigquery.SchemaField("employment_type", "STRING"),
    bigquery.SchemaField("date_posted", "TIMESTAMP"),
    bigquery.SchemaField("date_posted_month", "INTEGER"),
    bigquery.SchemaField("date_posted_year", "INTEGER"),
    bigquery.SchemaField("is_remote", "BOOLEAN"),
    bigquery.SchemaField("seniority", "STRING"),
    bigquery.SchemaField("apply_link", "STRING"),
    bigquery.SchemaField("load_date", "TIMESTAMP"),
]

client = bigquery.Client()

def create_if_staging_not_exists() -> bigquery.Table:

    logger.info(f"Checking Table ID {table_id} if it exists or not")
    try:
        table = client.get_table(table_id)
        logger.info(f"Table Already Exists for {table_id}")
        return table
    except NotFound:
        table = bigquery.Table(
            table_id,
            schema=schema
        )
        table = client.create_table(table)

        logger.info(f"Staging Table Created Successfully for {table_id}")
        return table

def load_dataframe_to_staging(df: pd.DataFrame):

    logger.info("Starting upload to staging table...")

    job_config = bigquery.LoadJobConfig(
        schema=schema,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
    )

    load_job = client.load_table_from_dataframe(
        dataframe=df,
        destination=table_id,
        job_config=job_config
    )

    load_job.result()

    logger.info(
        f"Successfully loaded {len(df)} rows into '{table_id}'."
    )

    return {
        "rows_loaded": len(df),
        "table": table_id
    }

