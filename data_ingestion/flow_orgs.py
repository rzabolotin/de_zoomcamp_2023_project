from loguru import logger
from prefect import flow, task
from services.DataExtractor import DataExtractor
from services.prefect_tasks import load_to_bq, save_table, save_to_gcp
from services.ProCultureAPI import ProCultureAPI
from services.utils import transform_date
from utils import enable_loguru_support

api = ProCultureAPI()


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


@flow(name="Load organizations")
def orgs_flow():
    enable_loguru_support()

    orgs_data = get_data_from_api()
    org_locales = extract_locales_from_orgs(orgs_data)

    orgs_file = save_table(orgs_data, "organizations")
    orgs_path = save_to_gcp(orgs_file)
    load_to_bq(orgs_path, "organizations")

    locales_file = save_table(org_locales, "organization_locales")
    locales_path = save_to_gcp(locales_file)
    load_to_bq(locales_path, "organization_locales")


if __name__ == "__main__":
    orgs_flow()
