from source.config import Config
from pathlib import Path


CONVERT_DICT = {
    'Y': True,
    'N': False,
}


class IniParser:
    def __init__(self, path: Path):
        self.path = path

    def parse(self):
        result = {'Books': []}
        with open(self.path, encoding='cp1251') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                if line.startswith('//'):
                    continue

                key, value = [res.strip() for res in line.split('=', maxsplit=1)]

                if value in CONVERT_DICT:
                    value = CONVERT_DICT[value]

                if key[-3:] == 'Qty':
                    value = int(value)

                if key == 'PathName':
                    result['Books'].append({key: value})

                if key in ('FullName', 'ShortName', 'ChapterQty'):
                    result['Books'][-1][key] = value

                result[key] = value
        return result


class Bible:
    def __init__(self, path: Path):
        self.path = path
        self.ini_path = None
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
        print(ini_parser.parse())


def get_bibles():
    bibles = {}
    for bible in Config.BIBLES_PATH.iterdir():
        if bible.is_dir():
            bibles[bible.stem] = Bible(bible)
    return bibles
