import json
import os
import yaml


def parse_file(filepath):

    _, extension = os.path.splitext(filepath.lower())

    with open(filepath, 'r') as file:
        content = file.read()

    if extension == '.json':
        return json.loads(content)
    elif extension in ('.yml', '.yaml'):
        return yaml.safe_load(content)
    else:
        raise ValueError(f"Unsupported file format: {extension}. ")
