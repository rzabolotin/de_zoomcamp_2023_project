import glob
from csv import DictReader
from pathlib import Path

from loguru import logger


class DataLoader:
    def __init__(self):
        self.data = []
        self.base_path = Path("data")

    def load_csv(self, path_prefix: str):
        logger.info(f"Loading files from pattern {path_prefix}")
        files = glob.glob(str(self.base_path / path_prefix))
        for file in files:
            logger.info(f"Loading from ... {file}")
            reader = DictReader(open(file, "r"))
            self.data.extend(reader)
