import io
import json
import os
from csv import DictWriter
from pathlib import Path

import pyarrow.csv as pw
import pyarrow.parquet as pq
from loguru import logger
from services.utils import ravel


class DataSaver:
    def __init__(self, file_type: str = "json", need_ravel: bool = True) -> None:
        if file_type not in ["json", "csv", "parquet"]:
            raise Exception("Unknown save type")

        self.file_type = file_type
        self.need_ravel = need_ravel
        self.base_path = Path("data")
        os.makedirs(self.base_path, exist_ok=True)

    def save(self, data: list, path: str):
        if self.need_ravel:
            ravel(data)

        logger.info(f"Saving to ... {os.path.abspath(path)}")

        if self.file_type == "json":
            filename = self.base_path / (path + ".json")
            with open(filename, "w") as outfile:
                json.dump(data, outfile)

        elif self.file_type == "csv":
            filename = self.base_path / (path + ".csv")
            fieldnames = DataSaver.get_fields(data)
            with open(filename, "w") as outfile:
                DataSaver.write_csv(data, fieldnames, outfile)

        elif self.file_type == "parquet":
            filename = self.base_path / (path + ".parquet")
            fieldnames = DataSaver.get_fields(data)
            with io.StringIO() as csv_file:
                DataSaver.write_csv(data, fieldnames, csv_file)
                csv_file.seek(0)
                csv_file = io.BytesIO(csv_file.read().encode("utf8"))
                table = pw.read_csv(csv_file)

            pq.write_table(table, filename)

        else:
            raise Exception("Unknown save type")

        return filename

    @staticmethod
    def get_fields(data: list):
        fieldnames = list()
        for row in data:
            fieldnames.extend([keys for keys in row.keys() if keys not in fieldnames])
        return fieldnames

    @staticmethod
    def write_csv(data, fieldnames, file_obj):
        writer = DictWriter(file_obj, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
