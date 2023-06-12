from source.config import Config
from pathlib import Path
from .helpers import IniParser


class Bible:
    def __init__(self, path: Path):
        self.path = path
        self.ini_path = None
        self.config = None

        self.parse_ini()

    def _init_ini_path(self):
        for ini_path in self.path.glob('*.ini'):
            if self.ini_path is not None:
                raise FileExistsError(f"Multiple ini files found for {self.path}")

            self.ini_path = ini_path
            break
        else:
            raise FileNotFoundError(f"Could not find ini file for {self.path}")

    def parse_ini(self):
        self._init_ini_path()
        ini_parser = IniParser(self.ini_path)
        self.config = ini_parser.parse()


def get_bibles():
    bibles = {}
    for bible in Config.BIBLES_PATH.iterdir():
        if bible.is_dir():
            bibles[bible.stem] = Bible(bible)
    return bibles
