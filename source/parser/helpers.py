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
