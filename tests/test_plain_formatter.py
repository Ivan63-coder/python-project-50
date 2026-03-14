import json
import os
import tempfile

from gendiff.generate_diff import generate_diff


def get_fixture_path(extension, filename):
    return os.path.join('tests', 'test_data', extension, filename)


def read_file(extension, filename):
    with open(get_fixture_path(extension, filename), 'r') as f:
        return f.read().strip()


def test_plain_formatter_flat():
    file1 = get_fixture_path('flat_json', 'file1.json')
    file2 = get_fixture_path('flat_json', 'file2.json')

    expected = read_file('flat_json', 'expected_plain.txt')
    result = generate_diff(file1, file2, 'plain')

    result_lines = sorted(result.split('\n'))
    expected_lines = sorted(expected.split('\n'))
    
    assert result_lines == expected_lines


def test_plain_formatter_nested():
    file1 = get_fixture_path('nested_json', 'file1.json')
    file2 = get_fixture_path('nested_json', 'file2.json')
    
    expected = read_file('nested_json', 'expected_plain.txt')
    result = generate_diff(file1, file2, 'plain')
    
    result_lines = sorted(result.split('\n'))
    expected_lines = sorted(expected.split('\n'))
    
    assert result_lines == expected_lines


def test_plain_formatter_with_numbers():
    data1 = {"timeout": 50, "retries": 3}
    data2 = {"timeout": 20, "retries": 3}

    file1 = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
    json.dump(data1, file1)
    file1.close()

    file2 = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
    json.dump(data2, file2)
    file2.close()

    try:
        result = generate_diff(file1.name, file2.name, 'plain')
        expected = "Property 'timeout' was updated. From 50 to 20"
        assert result == expected
    finally:
        os.unlink(file1.name)
        os.unlink(file2.name)


def test_plain_formatter_with_boolean():
    data1 = {"follow": True, "verbose": False}
    data2 = {"follow": False, "verbose": False}

    file1 = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
    json.dump(data1, file1)
    file1.close()

    file2 = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
    json.dump(data2, file2)
    file2.close()

    try:
        result = generate_diff(file1.name, file2.name, 'plain')
        expected = "Property 'follow' was updated. From true to false"
        assert result == expected
    finally:
        os.unlink(file1.name)
        os.unlink(file2.name)


def test_plain_formatter_with_null():
    data1 = {"value": None}
    data2 = {"value": "not null"}

    file1 = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
    json.dump(data1, file1)
    file1.close()

    file2 = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
    json.dump(data2, file2)
    file2.close()

    try:
        result = generate_diff(file1.name, file2.name, 'plain')
        expected = "Property 'value' was updated. From null to 'not null'"
        assert result == expected
    finally:
        os.unlink(file1.name)
        os.unlink(file2.name)


def test_plain_formatter_no_changes():
    data1 = {"key": "value"}
    data2 = {"key": "value"}

    file1 = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
    json.dump(data1, file1)
    file1.close()

    file2 = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
    json.dump(data2, file2)
    file2.close()

    try:
        result = generate_diff(file1.name, file2.name, 'plain')
        assert result == ""
    finally:
        os.unlink(file1.name)
        os.unlink(file2.name)
