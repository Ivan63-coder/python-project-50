import json
import tempfile
import os
from gendiff import generate_diff


def create_temp_file(content):
    with tempfile.NamedTemporaryFile(
        mode='w',
        suffix='.json',
        delete=False
    ) as f:
        json.dump(content, f, indent=2)
        return f.name


def normalize_string(s):
    return '\n'.join(line.rstrip() for line in s.split('\n'))


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
    - follow: false
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
        print("\nExpected:")
        print(repr(expected))
        print("\nResult:")
        print(repr(result))
        print("\nExpected lines:")
        for i, line in enumerate(expected.split('\n')):
            print(f"{i}: {repr(line)}")
        print("\nResult lines:")
        for i, line in enumerate(result.split('\n')):
            print(f"{i}: {repr(line)}")
        assert normalize_string(result) == normalize_string(expected)
    finally:
        os.unlink(file1)
        os.unlink(file2)


def test_generate_diff_with_bool_values():
    data1 = {
        "follow": True,
        "verbose": False
    }

    data2 = {
        "follow": False,
        "verbose": False
    }

    expected = """{
    - follow: true
    + follow: false
      verbose: false
}"""

    file1 = create_temp_file(data1)
    file2 = create_temp_file(data2)

    try:
        result = generate_diff(file1, file2)
        print("\nTest with bool values - Result:")
        print(result)
        assert normalize_string(result) == normalize_string(expected)
    finally:
        os.unlink(file1)
        os.unlink(file2)


def test_generate_diff_with_numbers():
    data1 = {
        "timeout": 50,
        "retries": 3
    }

    data2 = {
        "timeout": 20,
        "retries": 3
    }

    expected = """{
      retries: 3
    - timeout: 50
    + timeout: 20
}"""

    file1 = create_temp_file(data1)
    file2 = create_temp_file(data2)

    try:
        result = generate_diff(file1, file2)
        print("\nTest with numbers - Result:")
        print(result)
        print("\nExpected:")
        print(expected)
        assert normalize_string(result) == normalize_string(expected)
    finally:
        os.unlink(file1)
        os.unlink(file2)


def test_generate_diff_empty_files():
    data1 = {}
    data2 = {}

    expected = "{\n}"

    file1 = create_temp_file(data1)
    file2 = create_temp_file(data2)

    try:
        result = generate_diff(file1, file2)
        print("\nTest empty files - Result:")
        print(repr(result))
        print("\nExpected:")
        print(repr(expected))
        assert normalize_string(result) == normalize_string(expected)
    finally:
        os.unlink(file1)
        os.unlink(file2)


def test_generate_diff_all_keys_different():
    data1 = {
        "key1": "value1",
        "key2": "value2"
    }

    data2 = {
        "key3": "value3",
        "key4": "value4"
    }

    expected = """{
    - key1: value1
    - key2: value2
    + key3: value3
    + key4: value4
}"""

    file1 = create_temp_file(data1)
    file2 = create_temp_file(data2)

    try:
        result = generate_diff(file1, file2)
        print("\nTest all keys different - Result:")
        print(result)
        assert normalize_string(result) == normalize_string(expected)
    finally:
        os.unlink(file1)
        os.unlink(file2)


def test_generate_diff_with_mixed_keys():
    data1 = {
        "common": "same",
        "only_first": "first",
        "changed": "old"
    }

    data2 = {
        "common": "same",
        "only_second": "second",
        "changed": "new"
    }

    expected = """{
    - changed: old
    + changed: new
      common: same
    - only_first: first
    + only_second: second
}"""

    file1 = create_temp_file(data1)
    file2 = create_temp_file(data2)

    try:
        result = generate_diff(file1, file2)
        print("\nTest mixed keys - Result:")
        print(result)
        print("\nExpected:")
        print(expected)

        print("\nResult lines:")
        for i, line in enumerate(result.split('\n')):
            print(f"{i}: {repr(line)}")
        print("\nExpected lines:")
        for i, line in enumerate(expected.split('\n')):
            print(f"{i}: {repr(line)}")

        assert result == expected
    finally:
        os.unlink(file1)
        os.unlink(file2)
