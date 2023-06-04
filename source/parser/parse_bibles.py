from source.config import Config
from pathlib import Path
from dataclasses import dataclass


@dataclass
class Bible:
    path: Path
    name: str
    abbreviation: str


def get_bibles():
    bibles = {}
    for bible in Config.BIBLES_PATH.iterdir():
        print(bible)
        if bible.is_dir():
            bibles[bible.stem] = bible
    return bibles