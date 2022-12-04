import json
import jinja2
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
# from helpers.profile import read_profile
from helpers.connection import run_sql_on_target, get_type_from_credentials, convert_to_json
from helpers.config import get_profiling_from_config
from helpers.generic import resolve_path_to_frontend_public

from pathlib import Path, PurePath
from typing import Callable

from decimal import Decimal
from datetime import datetime, date

ConfigReader = Callable[[], list]

def read_from_config(key: str, config_reader: ConfigReader) -> list:
  return config_reader()[key] if key in config_reader() else []


def save_to_file(data, filename):
  filename.parent.mkdir(parents=True, exist_ok=True)
  with open(filename, 'w') as file:
    file.write(data)

def create_filename(filename, extension):
  filename = filename.with_suffix(f'.{extension}')
  return filename

def create_json_file(data, name, time, filename):
  filename.parent.mkdir(parents=True, exist_ok=True)
  wrapper = {
    "name": name,
    "created_at": time,
    'data': json.loads(data)
  }
  with open(filename, 'w') as file:
    json.dump(wrapper, file)


def main() -> None:
  target = get_type_from_credentials()
  print(f"Generate sql with Jinja for: {target}")

  templateLoader = jinja2.FileSystemLoader(
    encoding='utf-8-sig',
    searchpath = Path(__file__).parent.resolve() / 'jinja_templates' / target
  )
  templateEnv = jinja2.Environment(
    loader=templateLoader,
    extensions=['jinja2.ext.do']
  )

  _DISCOVER_TABLE = templateEnv.get_template("tables.sql")
  _PROFILE_TABLE = templateEnv.get_template("profile.sql")

  # It's probably overkill to insert result to a database, we'll use json instead
  _INSERT_PROFILE = templateEnv.get_template("insert.sql")

  tablesSQL = _DISCOVER_TABLE.render(
    table_type=read_from_config('table_types', get_profiling_from_config),
    include_schemas=read_from_config('include_schemas', get_profiling_from_config),
    exclude_schemas=read_from_config('exclude_schemas', get_profiling_from_config),
    separator=','
  )

  tables = run_sql_on_target(sql = tablesSQL)

  column_measures = read_from_config('column_measures', get_profiling_from_config)
  excluded_column_measures = read_from_config('excluded_column_measures', get_profiling_from_config)
  measures = [x for x in column_measures if x not in excluded_column_measures]

  profileSQL = _PROFILE_TABLE.render(
    items=tables,
    measures=measures
  )

  profiling = run_sql_on_target(sql = profileSQL)
  profiling_json = convert_to_json(profiling)

  folder_date = datetime.now().strftime("%Y%m%d")
  # print(f"Write to folder: {folder_date}")

  # path = Path(__file__).parent.parent.resolve() / 'output' / folder_date / 'profiling'
  # path = Path() / 'output' / folder_date / 'profiling'
  path = resolve_path_to_frontend_public() / 'output' / folder_date / 'profiling'
  print(f"Write to path: {path}")
  # print(test)
  filename = create_filename(path, 'json')


  # save_to_file(profiling_json, filename)
  create_json_file(data=profiling_json, name='profiling', time=datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f') , filename=filename)



if __name__ == "__main__":
  main()
  # print(Path() / 'output' / 'profiling')
  # cwd = Path(__file__).parent.resolve()
  # print(cwd)
  # print(resolve_path_to_frontend_public() / 'output' / 'profiling')


