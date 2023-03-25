import argparse

from loguru import logger
from services.DataExtractor import DataExtractor
from services.DataSaver import DataSaver
from services.ProCultureAPI import ProCultureAPI
from services.utils import transform_date

api = ProCultureAPI()
dataSaver = DataSaver(file_type="csv")


def main(params: argparse.Namespace) -> None:
    """Main function"""
    logger.info("Start loader")

    if params.type[0] == "orgs":
        orgs_data = api.get_organizations()
        orgs_data = transform_date(
            orgs_data, ["updateDate", "pushkaRulesAccepted_date", "createDate"]
        )
        org_locales = DataExtractor.extract_locales_from_orgs(orgs_data)

        filename = "organizations"
        dataSaver.save(orgs_data, filename)

        filename = "organization_locales"
        dataSaver.save(org_locales, filename)

    elif params.type[0] == "locales":
        data = api.get_locales()
        dataSaver.save(data, "locales")

    elif params.type[0] == "tags":
        data = api.get_tags()
        dataSaver.save(data, "tags")

    elif params.type[0] == "events":
        start_chunk = params.start_chunk
        end_chunk = params.end_chunk

        suffix = f"_{start_chunk}_{end_chunk}"

        data_events = api.get_events(start_chunk, end_chunk)
        event_tags = DataExtractor.extract_tags_from_events(data_events)
        event_places = DataExtractor.extract_places_from_orgs(data_events)
        event_seances = DataExtractor.extract_seances_from_event_places(event_places)
        event_place_locales = DataExtractor.extract_locales_from_places(event_places)

        data_events = transform_date(
            data_events, ["updateDate", "start", "end", "createDate"]
        )
        event_seances = transform_date(event_seances, ["start", "end"])

        dataSaver.save(data_events, "events_" + suffix)
        dataSaver.save(event_tags, "event_tags_" + suffix)
        dataSaver.save(event_places, "event_places_" + suffix)
        dataSaver.save(event_seances, "event_seances_" + suffix)
        dataSaver.save(event_place_locales, "event_place_locales" + suffix)

    else:
        logger.error("Unknown type")
        return

    logger.success("Done!")


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "type", type=str, nargs=1, choices=["events", "orgs", "locales", "tags"]
    )
    arg_parser.add_argument("--start_chunk", type=int, default=0)
    arg_parser.add_argument("--end_chunk", type=int, default=100000)

    args = arg_parser.parse_args()
    main(args)
