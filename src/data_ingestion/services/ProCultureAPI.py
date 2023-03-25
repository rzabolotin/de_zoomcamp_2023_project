import logging
import os
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
        self.test_count = 300

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

        logger.debug(f"Getting data for {method} offset {params.get('offset')}")

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
            "organizationTypes" "hasCinemaTerminal",
        ]

        params = {"fields": ",".join(fields), "limit": self.limit, "offset": 0}

        raw_data = self._get_data("organizations", params)
        if not raw_data or "organizations" not in raw_data:
            raise Exception("Organizations not found in API answer")

        total = raw_data["total"]

        logger.info(
            f'Load first {len(raw_data["organizations"])} organizations from {total}'
        )

        carry = []
        carry.extend(raw_data["organizations"])
        params["offset"] += self.limit

        err_counter = 0
        if self.test_count:
            logging.warning("ProCultureAPi in TEST MODE, got only 2000 records")
            total = self.test_count

        while params["offset"] <= total:
            raw_data = self._get_data("organizations", params)
            if not raw_data or "organizations" not in raw_data:
                logger.warning("Got empty result from API")
                err_counter += 1
                if err_counter < 5:
                    continue
                raise Exception("Got 5 empty response in a raw")

            carry.extend(raw_data["organizations"])
            params["offset"] += self.limit

        return carry
