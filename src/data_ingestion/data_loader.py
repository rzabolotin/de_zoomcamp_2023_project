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
    else:
        logger.error("Unknown type")
        return

    logger.success("Done!")


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("type", type=str, nargs=1, choices=["events", "orgs"])

    args = arg_parser.parse_args()
    main(args)
