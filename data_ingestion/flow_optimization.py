from loguru import logger
from prefect import flow, task
from services.big_query import create_partition_table
from services.utils import check_environment_google_cloud


@task(name="Create partition table events_partitioned")
def make_partition_table():
    logger.info(f"Creating partition table for events")
    create_partition_table(
        new_table="events_partitioned",
        source_table="events_raw",
        partition_field="start",
    )


@flow(name="Make partition tables")
def partitioning_flow():
    check_environment_google_cloud()
    make_partition_table()


if __name__ == "__main__":
    partitioning_flow()
