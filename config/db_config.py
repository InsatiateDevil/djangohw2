from pathlib import Path
from configparser import ConfigParser

BASE_DIR = Path(__file__).resolve().parent.parent
FILE_PATH = Path.joinpath(BASE_DIR, 'config', 'database.ini')


def db_config_parser(filepath=FILE_PATH, section="postgresql"):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filepath)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} is not found in the {filepath} file.')
    return db
