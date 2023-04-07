import os

from google.cloud import bigquery
from loguru import logger

bigquery_client = bigquery.Client()

if any(
    [
        env not in os.environ
        for env in [
            "GOOGLE_PROJECT_ID",
            "GOOGLE_BQ_DATASET",
            "GOOGLE_DATA_LAKE_BUCKET_NAME",
        ]
    ]
):
    raise Exception("Not found environment variables for Google cloud")

GOOGLE_PROJECT_ID = os.environ.get("GOOGLE_PROJECT_ID")
BQ_DATASET = os.environ.get("GOOGLE_BQ_DATASET")
DATA_LAKE_BUCKET_NAME = f"gs://{os.environ.get('GOOGLE_DATA_LAKE_BUCKET_NAME')}"


def load_to_bigquery(table_name: str, filepath: str, clean_table: bool = True) -> str:
    table_id = f"{GOOGLE_PROJECT_ID}.{BQ_DATASET}.{table_name}"
    uri = f"{DATA_LAKE_BUCKET_NAME}/{filepath}"

    logger.info("Start loading to BigQuery")

    if clean_table:
        bigquery_client.delete_table(table_id, not_found_ok=True)
        logger.info(f"Table {table_name} deleted")

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.PARQUET,
    )

    load_job = bigquery_client.load_table_from_uri(uri, table_id, job_config=job_config)

    load_job.result()  # Waits for the job to complete.

    destination_table = bigquery_client.get_table(table_id)
    logger.info(f"Loaded {destination_table.num_rows} rows.")

    return filepath
