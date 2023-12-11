import json
from pathlib import Path

from typing import Dict


DATA_PATH = Path(__file__).parent.resolve().joinpath("data")


def load_json(data_file: Path) -> Dict:
    with data_file.open(encoding="utf-8") as d:
        return json.load(d)
