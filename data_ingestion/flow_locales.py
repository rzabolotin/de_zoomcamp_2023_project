from loguru import logger
from prefect import flow, task
from services.prefect_tasks import load_to_bq, save_table, save_to_gcp
from services.ProCultureAPI import ProCultureAPI
from services.utils import (
    enable_loguru_support,
    check_environment_cultura_api,
    check_environment_google_cloud,
)

api = ProCultureAPI()


@task(name="Loading locales from API")
def get_data_from_api():
    logger.info("Start loader")
    return api.get_locales()


@flow(name="Load locales")
def locales_flow():
    enable_loguru_support()
    check_environment_cultura_api()
    check_environment_google_cloud()

    locales_data = get_data_from_api()
    locales_file = save_table(locales_data, "locales")
    locales_path = save_to_gcp(locales_file)
    load_to_bq(locales_path, "locales")


if __name__ == "__main__":
    locales_flow()
