import logging
import os
from datetime import datetime
from typing import Union

import requests
from loguru import logger


class ProCultureAPI:
    """Class to handle the ProCulture API"""

    def __init__(self):
        self.base_url = "https://pro.culture.ru/api/2.5/"
        self.api_key = os.environ.get("CULTURE_API_KEY", None)
        if "CULTURE_API_KEY" not in os.environ:
            raise Exception("Not found API KEY for culture.ru")

        self.limit = 100
        self.test_count = 0

    def _get_data(
        self, method: str, params: Union[dict, None] = None
    ) -> Union[dict, None]:
        """Get data from API synchronously

        :param method: API method
        :param params: additional params for request
        :return: dict from json or None if error
        """
        url = self.base_url + method
        if not params:
            params = {}

        params["apiKey"] = self.api_key

        logger.info(f"Getting data for {method} offset {params.get('offset')}")

        try:
            data = requests.get(url, params).json()
        except Exception as e:
            logger.error("Error: {error}", error=e)
            return None

        if "error" in data:
            logger.error(
                "Error: {error}, Message: {message}",
                error=data["error"],
                message=data["userMessage"],
            )
            return None

        return data

    def get_organizations(self):
        """Get organizations list"""
        method_name = "organizations"
        fields = [
            "_id",
            "createDate",
            "localeIds",
            "nameShort",
            "type",
            "updateDate",
            "category",
            "status",
            "subordination",
            "inn",
            "isPushkinsCard",
            "pushkaRulesAccepted",
            "isAccessible",
            "ticketsSold",
            "isTicketsSystem",
            "status",
            "ratingRegion",
            "isPushkaRequested",
            "organizationTypes",
            "hasCinemaTerminal",
        ]

        params = {"fields": ",".join(fields), "limit": self.limit, "offset": 0}

        raw_data = self._get_data(method_name, params)
        if not raw_data or method_name not in raw_data:
            raise Exception("Empty API answer")

        total = raw_data["total"]

        logger.info(f"Load first {len(raw_data[method_name])} rows from {total}")

        carry = []
        carry.extend(raw_data[method_name])
        params["offset"] += self.limit

        err_counter = 0
        if self.test_count:
            logging.warning(
                f"ProCultureAPI in TEST MODE, got only {self.test_count} records"
            )
            total = self.test_count

        while params["offset"] <= total:
            raw_data = self._get_data(method_name, params)
            if not raw_data or method_name not in raw_data:
                logger.warning("Got empty result from API")
                err_counter += 1
                if err_counter < 5:
                    continue
                raise Exception("Got 5 empty response in a raw")

            carry.extend(raw_data[method_name])
            params["offset"] += self.limit

        return carry

    def get_locales(self):
        """Get locales"""
        method_name = "locales"
        fields = ["_id", "name", "timezone", "parentId", "fias", "population", "stats"]

        params = {"fields": ",".join(fields), "limit": self.limit, "offset": 0}

        raw_data = self._get_data(method_name, params)
        if not raw_data or method_name not in raw_data:
            raise Exception("Empty API answer")

        total = raw_data["total"]

        logger.info(f"Load first {len(raw_data[method_name])} rows from {total}")

        carry = []
        carry.extend(raw_data[method_name])
        params["offset"] += self.limit

        err_counter = 0
        if self.test_count:
            logging.warning(
                f"ProCultureAPi in TEST MODE, got only {self.test_count} records"
            )
            total = self.test_count

        while params["offset"] <= total:
            raw_data = self._get_data(method_name, params)
            if not raw_data or method_name not in raw_data:
                logger.warning("Got empty result from API")
                err_counter += 1
                if err_counter < 5:
                    continue
                raise Exception("Got 5 empty response in a raw")

            carry.extend(raw_data[method_name])
            params["offset"] += self.limit

        return carry

    def get_tags(self):
        """Get tags list"""
        method_name = "tags"

        params = {"limit": self.limit, "offset": 0}

        raw_data = self._get_data(method_name, params)
        if not raw_data or method_name not in raw_data:
            raise Exception("Empty API answer")

        total = raw_data["total"]

        logger.info(f"Load first {len(raw_data[method_name])} rows from {total}")

        carry = []
        carry.extend(raw_data[method_name])
        params["offset"] += self.limit

        err_counter = 0
        if self.test_count:
            logging.warning(
                f"ProCultureAPi in TEST MODE, got only {self.test_count} records"
            )
            total = self.test_count

        while params["offset"] <= total:
            raw_data = self._get_data(method_name, params)
            if not raw_data or method_name not in raw_data:
                logger.warning("Got empty result from API")
                err_counter += 1
                if err_counter < 5:
                    continue
                raise Exception("Got 5 empty response in a raw")

            carry.extend(raw_data[method_name])
            params["offset"] += self.limit

        return carry

    def get_events(self, start_chunk: int, end_chunk: int):
        """Get events list"""
        method_name = "events"

        fields = [
            "_id",
            "name",
            "ageRestriction",
            "tags",
            "isFree",
            "price",
            "maxPrice",
            "places",
            "responsible",
            "benefits",
            "needCheck",
            "status",
            "updateDate",
            "start",
            "end",
            "isAccesible",
            "createDate",
            "isAccepted",
            "accepteDate",
            "categoryName",
            "organization",
            "extraField",
            "organizerPlace",
            "isPushkinsCard",
            "pushkeExpertType",
            "releaseDate",
            "genres",
            "countries",
            "statusPushka",
            "hasCinemaTerminal",
        ]

        logger.info(f"Load events from {start_chunk} to {end_chunk}")

        params = {
            "fields": ",".join(fields),
            "start": datetime(2021, 1, 1).timestamp() * 1000,
            "limit": self.limit,
            "offset": start_chunk,
        }

        raw_data = self._get_data(method_name, params)
        if not raw_data or method_name not in raw_data:
            raise Exception("Empty API answer")

        total = raw_data["total"]

        logger.info(f"Load first {len(raw_data[method_name])} rows from {total}")

        carry = []
        carry.extend(raw_data[method_name])
        params["offset"] += self.limit

        err_counter = 0
        if self.test_count:
            logging.warning(
                f"ProCultureAPi in TEST MODE, got only {self.test_count} records"
            )
            total = params["offset"] + self.test_count

        while params["offset"] <= total and params["offset"] <= end_chunk:
            raw_data = self._get_data(method_name, params)
            if not raw_data or method_name not in raw_data:
                logger.warning("Got empty result from API")
                err_counter += 1
                if err_counter < 5:
                    continue
                raise Exception("Got 5 empty response in a raw")

            carry.extend(raw_data[method_name])
            params["offset"] += self.limit

        return carry
