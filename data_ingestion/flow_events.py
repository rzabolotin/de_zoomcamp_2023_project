from loguru import logger
from prefect import flow, task
from services.DataExtractor import DataExtractor
from services.prefect_tasks import load_to_bq, save_table, save_to_gcp
from services.ProCultureAPI import ProCultureAPI
from services.utils import transform_date
from utils import enable_loguru_support

api = ProCultureAPI()


@task(name="Loading events from API")
def get_data_from_api(start_chunk:int, end_chunk:int):
    logger.info(f"Start loader {start_chunk} - {end_chunk}")
    return api.get_events(start_chunk, end_chunk)


@task(name="Extracting tags from events")
def extract_tags_from_events(orgs_data):
    return DataExtractor.extract_tags_from_events(orgs_data)


@task(name="Extracting places from events")
def extract_places_from_events(orgs_data):
    return DataExtractor.extract_places_from_orgs(orgs_data)


@task(name="Extracting seances from events")
def extract_seances_from_places(places_data):
    return DataExtractor.extract_seances_from_event_places(places_data)


@task(name="Extracting locales from events")
def extract_locales_from_places(orgs_places):
    return DataExtractor.extract_locales_from_places(orgs_places)



@flow(name="Load events by chunks")
def events_chunk_flow(start_chunk:int, end_chunk:int):
    enable_loguru_support()

    suffix = f"{start_chunk}-{end_chunk}"
    clean_table = True if start_chunk == 0 else False

    events_data = get_data_from_api(start_chunk, end_chunk)
    event_tags = extract_tags_from_events(events_data)
    event_places = extract_places_from_events(events_data)
    event_seances = extract_seances_from_places(event_places)
    event_locales = extract_locales_from_places(event_places)

    events_data = transform_date(
        events_data, ["updateDate", "start", "end", "createDate"]
    )
    event_seances = transform_date(event_seances, ["start", "end"])

    events_data = save_table(events_data, "events_"+suffix)
    events_path = save_to_gcp(events_data)
    load_to_bq(events_path, "events", clean_table=clean_table)

    file = save_table(event_tags, "event_tags_"+suffix)
    if file:
        path = save_to_gcp(file)
        load_to_bq(path, "event_tags", clean_table=clean_table)

    file = save_table(event_places, "event_places_"+suffix)
    if file:
        path = save_to_gcp(file)
        load_to_bq(path, "event_places", clean_table=clean_table)

    file = save_table(event_seances, "event_seances_"+suffix)
    if file:
        path = save_to_gcp(file)
        load_to_bq(path, "event_seances", clean_table=clean_table)

    file = save_table(event_locales, "event_locales_"+suffix)
    if file:
        path = save_to_gcp(file)
        load_to_bq(path, "event_locales")


@flow(name="Load events")
def events_flow():
    max_events = api.get_events_count()
    logger.info(f"Max events: {max_events}")
    chuk_size = 1000

    for i in range(0, max_events, chuk_size):
        events_chunk_flow(i, i+chuk_size)


if __name__ == "__main__":
    events_flow()
