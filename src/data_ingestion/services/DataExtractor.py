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
