from typing import List

from loguru import logger


class DataExtractor:
    @staticmethod
    def extract_locales_from_orgs(
        orgs_data: List[dict], remove_origin: bool = True
    ) -> List[dict]:
        logger.info("Extracting locales from organizations ...")
        locales = []
        for org in orgs_data:
            if "localeIds" in org:
                for locale_id in org["localeIds"]:
                    locales.append({"org_id": org["_id"], "locale_id": locale_id})
                if remove_origin:
                    del org["localeIds"]
        return locales

    @staticmethod
    def extract_tags_from_events(
        event_data: List[dict], remove_origin: bool = True
    ) -> List[dict]:
        logger.info("Extracting tags from events ...")
        tags = []
        for event in event_data:
            if "tags" in event:
                for tag in event["tags"]:
                    tag["event_id"] = event["_id"]
                    tags.append(tag)
                if remove_origin:
                    del event["tags"]
        return tags

    @staticmethod
    def extract_places_from_orgs(
        event_data: List[dict], remove_origin: bool = True
    ) -> List[dict]:
        logger.info("Extracting places from events ...")
        places = []
        for event in event_data:
            if "places" in event:
                for place in event["places"]:
                    place["event_id"] = event["_id"]
                    places.append(place)
                if remove_origin:
                    del event["places"]
        return places

    @staticmethod
    def extract_seances_from_event_places(
        places_data: List[dict], remove_origin: bool = True
    ) -> List[dict]:
        logger.info("Extracting seances from events ...")
        seances = []
        for place_event in places_data:
            if "seances" in place_event:
                for place in place_event["seances"]:
                    if "_id" in place:
                        place["place_id"] = place_event["_id"]
                    place["event_id"] = place_event["event_id"]

                    seances.append(place)
                if remove_origin:
                    del place_event["seances"]
        return seances

    @staticmethod
    def extract_locales_from_places(
        event_places_data: List[dict], remove_origin: bool = True
    ) -> List[dict]:
        logger.info("Extracting locales from organizations ...")
        locales = []
        for event_place in event_places_data:
            if "localeIds" in event_place:
                for locale_id in event_place["localeIds"]:
                    if "_id" in event_place:
                        locales.append(
                            {
                                "event_place_id": event_place["_id"],
                                "event_id": event_place["event_id"],
                                "locale_id": locale_id,
                            }
                        )
                    else:
                        locales.append(
                            {
                                "event_id": event_place["event_id"],
                                "locale_id": locale_id,
                            }
                        )
                if remove_origin:
                    del event_place["localeIds"]
        return locales
