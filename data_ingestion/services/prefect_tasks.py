import os

from prefect import task
from prefect_gcp import GcsBucket
from services.big_query import load_to_bigquery
from services.DataSaver import DataSaver

data_saver = DataSaver(file_type="parquet")


@task(name="Saving table")
def save_table(data, filename):
    return data_saver.save(data, filename)


@task(name="Move file to GCS")
def save_to_gcp(path: str) -> None:
    to_path = os.path.basename(path)
    gcs_data_lake = GcsBucket.load("gcs-data-lake")
    gcs_data_lake.upload_from_path(from_path=path, to_path=to_path)
    return to_path


@task(name="Load table to BigQuery")
def load_to_bq(path: str, table_name: str, clean_table: bool = True) -> str:
    return load_to_bigquery(table_name, path, clean_table=clean_table)
