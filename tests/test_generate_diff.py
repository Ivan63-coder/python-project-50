import json
import tempfile
import os
from gendiff import generate_diff


def create_temp_file(content):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(content, f)
        return f.name


def test_generate_diff():
    data1 = {
        "host": "hexlet.io",
        "timeout": 50,
        "proxy": "123.234.53.22",
        "follow": False
    }

    data2 = {
        "timeout": 20,
        "verbose": True,
        "host": "hexlet.io"
    }

    expected = """{
    host: hexlet.io
  - proxy: 123.234.53.22
  - timeout: 50
  + timeout: 20
  + verbose: true
}"""

    file1 = create_temp_file(data1)
    file2 = create_temp_file(data2)

    try:
        result = generate_diff(file1, file2)
        assert result == expected
    finally:
        os.unlink(file1)
        os.unlink(file2)
