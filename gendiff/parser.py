import json
import os


def parse_file(filepath):
    _, extension = os.path.splitext(filepath.lower())

    with open(filepath, 'r') as file:
        content = file.read()

    if extension == '.json':
        return json.loads(content)
    else:
        raise ValueError(f"Unsupported file format: {extension}")
