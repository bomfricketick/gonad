from typing import Any, Dict, Optional
import os
import yaml
from pathlib import Path

# the C version is faster, but it doesn't always exist
try:
    from yaml import CLoader as Loader, CSafeLoader as SafeLoader, CDumper as Dumper
except ImportError:
    from yaml import Loader, SafeLoader, Dumper  # type: ignore  # noqa: F401


YAML_ERROR_MESSAGE = """
Syntax error near line {line_number}
------------------------------
{nice_error}
Raw Error:
------------------------------
{raw_error}
""".strip()


INVALID_PROFILE_MESSAGE = """
encountered an error while trying to read your profiles.yml file.
{error_string}
"""


def line_no(i, line, width=3):
    line_number = str(i).ljust(width)
    return "{}| {}".format(line_number, line)


def prefix_with_line_numbers(string, no_start, no_end):
    line_list = string.split("\n")

    numbers = range(no_start, no_end)
    relevant_lines = line_list[no_start:no_end]

    return "\n".join([line_no(i + 1, line) for (i, line) in zip(numbers, relevant_lines)])


def contextualized_yaml_error(raw_contents, error):
    mark = error.problem_mark

    min_line = max(mark.line - 3, 0)
    max_line = mark.line + 4

    nice_error = prefix_with_line_numbers(raw_contents, min_line, max_line)

    return YAML_ERROR_MESSAGE.format(
        line_number=mark.line + 1, nice_error=nice_error, raw_error=error
    )

def safe_load(contents) -> Optional[Dict[str, Any]]:
    return yaml.load(contents, Loader=SafeLoader)


def load_yaml_text(contents, path=None):
    try:
        return safe_load(contents)
    except (yaml.scanner.ScannerError, yaml.YAMLError) as e:
        if hasattr(e, "problem_mark"):
            error = contextualized_yaml_error(contents, e)
        else:
            error = str(e)


def load_file_contents(path: str, strip: bool = True) -> str:
    with open(path, "rb") as handle:
        to_return = handle.read().decode("utf-8")

    if strip:
        to_return = to_return.strip()

    return to_return

def read_profile(profiles_dir: str) -> Dict[str, Any]:
    path = os.path.join(profiles_dir, "profiles.yml")

    contents = None
    if os.path.isfile(path):
        try:
            contents = load_file_contents(path, strip=False)
            yaml_content = load_yaml_text(contents)
            if not yaml_content:
                msg = f"The profiles.yml file at {path} is empty"
            return yaml_content
        except:
            print('failed')
    return {}


def read_file(path: str) -> Dict[str, Any]:
    contents = None
    if os.path.isfile(path):
        try:
            contents = load_file_contents(path, strip=False)
            yaml_content = load_yaml_text(contents)
            if not yaml_content:
                msg = f"The file at {path} is empty"
                return msg
            return yaml_content
        except:
            print('failed')

    return {}


def keys_exists(element, *keys):
    '''
    Check if *keys (nested) exists in `element` (dict).
    '''
    if not isinstance(element, dict):
        raise AttributeError('keys_exists() expects dict as first argument.')
    if len(keys) == 0:
        raise AttributeError('keys_exists() expects at least two arguments, one given.')

    _element = element
    for key in keys:
        try:
            _element = _element[key]
        except KeyError:
            return False
    return True

def resolve_grandparent_path():
    current_dir = Path(__file__).parent.resolve()
    grandparent_dir = current_dir.parent.resolve()
    return grandparent_dir