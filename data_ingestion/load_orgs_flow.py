from loguru import logger
from prefect import flow, task
from prefect_gcp import GcsBucket
from services.DataExtractor import DataExtractor
from services.DataSaver import DataSaver
from services.ProCultureAPI import ProCultureAPI
from services.utils import transform_date
from utils import enable_loguru_support

api = ProCultureAPI()
data_saver = DataSaver(file_type="parquet")
gcs_data_lake = GcsBucket.load("gcs-data-lake")

# https://cloud.google.com/bigquery/docs/loading-data-cloud-storage-parquet#python


@task(name="Loading organizations from API")
def get_data_from_api():
    logger.info("Start loader")
    orgs_data = api.get_organizations()
    orgs_data = transform_date(
        orgs_data, ["updateDate", "pushkaRulesAccepted_date", "createDate"]
    )
    return orgs_data


@task(name="Extracting locales from organizations")
def extract_locales_from_orgs(orgs_data):
    org_locales = DataExtractor.extract_locales_from_orgs(orgs_data)
    return org_locales


@task(name="Saving table")
def save_table(data, filename):
    return data_saver.save(data, filename)


@task(name="Move file to GCS")
def save_to_gcp(path: str) -> None:
    gcs_data_lake.upload_from_path(from_path=path, to_path=path)


@flow(name="Load organizations")
def orgs_flow():
    enable_loguru_support()

    orgs_data = get_data_from_api()
    org_locales = extract_locales_from_orgs(orgs_data)

    orgs_file = save_table(orgs_data, "organizations")
    locales_file = save_table(org_locales, "organization_locales")

    save_to_gcp(orgs_file)
    save_to_gcp(locales_file)


if __name__ == "__main__":
    orgs_flow()
