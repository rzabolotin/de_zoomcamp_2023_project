import json
import os
from csv import DictWriter
from pathlib import Path

from loguru import logger
from services.utils import ravel


class DataSaver:
    def __init__(self, file_type: str = "json", need_ravel: bool = True) -> None:
        if file_type not in ["json", "csv"]:
            raise Exception("Unknown save type")

        self.file_type = file_type
        self.need_ravel = need_ravel
        self.base_path = Path("data")
        os.makedirs(self.base_path, exist_ok=True)

    def save(self, data: list, path: str):
        if self.need_ravel:
            ravel(data)

        logger.info(f"Saving to ... {path}")

        if self.file_type == "json":
            with open(self.base_path / (path + ".json"), "w") as outfile:
                json.dump(data, outfile)
        if self.file_type == "csv":
            fieldnames = list()
            for row in data:
                fieldnames.extend(
                    [keys for keys in row.keys() if keys not in fieldnames]
                )

            writer = DictWriter(
                open(self.base_path / (path + ".csv"), "w"), fieldnames=fieldnames
            )
            writer.writeheader()
            writer.writerows(data)

        else:
            raise Exception("Unknown save type")
