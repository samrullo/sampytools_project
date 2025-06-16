import json
import pathlib


def read_json_file(json_filepath: pathlib.Path, encoding: str = "utf-8") -> dict:
    """
    Read a JSON file into a dictionary
    :param json_filepath:
    :param encoding:
    :return:
    """
    return json.loads(json_filepath.read_text(encoding=encoding))
