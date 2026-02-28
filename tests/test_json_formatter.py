import json
import os
import tempfile
from gendiff import generate_diff


def get_fixture_path(extension, filename):
    return os.path.join('tests', 'test_data', extension, filename)


def read_file(extension, filename):
    with open(get_fixture_path(extension, filename), 'r') as f:
        return f.read().strip()


def test_json_formatter_flat():
    file1 = get_fixture_path('flat_json', 'file1.json')
    file2 = get_fixture_path('flat_json', 'file2.json')

    result = generate_diff(file1, file2, 'json')

    result_data = json.loads(result)

    assert isinstance(result_data, list)

    assert len(result_data) == 5

    for item in result_data:
        assert 'key' in item
        assert 'status' in item
        assert item['status'] in ['added', 'removed', 'changed', 'unchanged']

        if item['status'] == 'added':
            assert 'value' in item
        elif item['status'] == 'removed':
            assert 'value' in item
        elif item['status'] == 'changed':
            assert 'old_value' in item
            assert 'new_value' in item
        elif item['status'] == 'unchanged':
            assert 'value' in item


def test_json_formatter_nested():
    file1 = get_fixture_path('nested_json', 'file1.json')
    file2 = get_fixture_path('nested_json', 'file2.json')

    result = generate_diff(file1, file2, 'json')

    result_data = json.loads(result)

    assert isinstance(result_data, list)

    common_node = next(
        (item for item in result_data if item['key'] == 'common'), None
    )
    assert common_node is not None
    assert common_node['status'] == 'nested'
    assert 'children' in common_node
    assert isinstance(common_node['children'], list)


def test_json_formatter_roundtrip():
    file1 = get_fixture_path('nested_json', 'file1.json')
    file2 = get_fixture_path('nested_json', 'file2.json')

    result = generate_diff(file1, file2, 'json')

    parsed = json.loads(result)

    assert isinstance(parsed, list)

    keys = [item['key'] for item in parsed]
    assert 'common' in keys
    assert 'group1' in keys
    assert 'group2' in keys or 'group3' in keys


def test_json_formatter_no_changes():
    file1 = get_fixture_path('flat_json', 'file1.json')

    result = generate_diff(file1, file1, 'json')
    result_data = json.loads(result)

    for item in result_data:
        assert item['status'] == 'unchanged'


def test_json_formatter_all_changes():
    data1 = {"key1": "value1"}
    data2 = {"key2": "value2"}

    file1 = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
    json.dump(data1, file1)
    file1.close()

    file2 = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
    json.dump(data2, file2)
    file2.close()

    try:
        result = generate_diff(file1.name, file2.name, 'json')
        result_data = json.loads(result)

        assert len(result_data) == 2
        statuses = [item['status'] for item in result_data]
        assert 'removed' in statuses
        assert 'added' in statuses
    finally:
        os.unlink(file1.name)
        os.unlink(file2.name)


def test_json_formatter_with_complex_values():
    data1 = {
        "simple": "value",
        "nested": {"key": "value"},
        "array": [1, 2, 3]
    }
    data2 = {
        "simple": "changed",
        "nested": {"key": "new_value"},
        "array": [1, 2, 3]
    }

    file1 = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
    json.dump(data1, file1)
    file1.close()

    file2 = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
    json.dump(data2, file2)
    file2.close()

    try:
        result = generate_diff(file1.name, file2.name, 'json')
        result_data = json.loads(result)

        assert len(result_data) == 3

        simple_node = next(
            (item for item in result_data if item['key'] == 'simple'), None
        )
        assert simple_node['status'] == 'changed'
        assert simple_node['old_value'] == 'value'
        assert simple_node['new_value'] == 'changed'

        nested_node = next(
            (item for item in result_data if item['key'] == 'nested'), None
        )
        assert nested_node['status'] == 'nested'
        assert len(nested_node['children']) > 0

        array_node = next(
            (item for item in result_data if item['key'] == 'array'), None
        )
        assert array_node['status'] == 'unchanged'
    finally:
        os.unlink(file1.name)
        os.unlink(file2.name)
