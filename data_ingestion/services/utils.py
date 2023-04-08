from datetime import datetime
import os

from prefect import get_run_logger
from prefect_gcp import GcsBucket


def ravel(data: list):
    modified = False
    for row in data:
        dict_keys = [key for key in row if type(row[key]) == dict]
        for dict_key in dict_keys:
            for valKey, value in row[dict_key].items():
                if dict_key == "organization" and valKey != "_id":
                    continue
                if dict_key in [
                    "address",
                    "image",
                    "locale",
                    "mapPosition",
                    "schedule",
                ]:
                    continue
                row[dict_key + "_" + valKey] = value
            del row[dict_key]
            modified = True
    if modified:
        ravel(data)


def transform_date(data, date_columns):
    for row in data:
        for column in date_columns:
            if column in row:
                row[column] = datetime.fromtimestamp(row[column] / 1000).date()

    return data


def enable_loguru_support() -> None:
    """Redirect loguru logging messages to the prefect run logger.
    This function should be called from within a Prefect task or flow before calling any module that uses loguru.
    This function can be safely called multiple times.
    Example Usage:
    from prefect import flow
    from loguru import logger
    from prefect_utils import enable_loguru_support # import this function in your flow from your module
    @flow()
    def myflow():
        logger.info("This is hidden from the Prefect UI")
        enable_loguru_support()
        logger.info("This shows up in the Prefect UI")
    """
    # import here for distributed execution because loguru cannot be pickled.
    from loguru import logger  # pylint: disable=import-outside-toplevel

    run_logger = get_run_logger()
    logger.remove()
    log_format = "{name}:{function}:{line} - {message}"
    logger.add(
        run_logger.debug,
        filter=lambda record: record["level"].name == "DEBUG",
        level="TRACE",
        format=log_format,
    )
    logger.add(
        run_logger.warning,
        filter=lambda record: record["level"].name == "WARNING",
        level="TRACE",
        format=log_format,
    )
    logger.add(
        run_logger.error,
        filter=lambda record: record["level"].name == "ERROR",
        level="TRACE",
        format=log_format,
    )
    logger.add(
        run_logger.critical,
        filter=lambda record: record["level"].name == "CRITICAL",
        level="TRACE",
        format=log_format,
    )
    logger.add(
        run_logger.info,
        filter=lambda record: record["level"].name
        not in ["DEBUG", "WARNING", "ERROR", "CRITICAL"],
        level="TRACE",
        format=log_format,
    )


def check_environment_google_cloud():
    required_env = [
        "GOOGLE_PROJECT_ID",
        "GOOGLE_BQ_DATASET",
        "GOOGLE_DATA_LAKE_BUCKET_NAME",
    ]

    if any([env not in os.environ for env in required_env]):
        raise Exception("Not found environment variables for Google cloud")

    GcsBucket.load("gcs-data-lake")


def check_environment_cultura_api():
    if "CULTURE_API_KEY" not in os.environ:
        raise Exception("Not found API KEY for culture.ru")


