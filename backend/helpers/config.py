import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from helpers.profile import read_file, keys_exists, resolve_grandparent_path
from pathlib import Path

def get_profiling_from_config():
    """Read config and return profiling"""
    config = read_file(path= resolve_grandparent_path() / 'config.yml')
    # print(json.dumps(profile, indent=4))
    if not keys_exists(config, 'project'):
        return('the root key "project" is missing from config.yml')
    if not keys_exists(config, 'project', 'profiling'):
        return('the key "profiling" is missing from config.yml')
    profiling = config['project']['profiling']
    return profiling


# test = get_profiling_from_config()
# print(test['table_types'])