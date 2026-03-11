import os

import pytest

from gendiff.generate_diff import generate_diff


def get_fixture_path(filename):
    return os.path.join('tests', 'test_data', 'flat_json', filename)


def read_file(filename):
    with open(get_fixture_path(filename), 'r') as f:
        return f.read()


def test_generate_diff_flat_json():
    file1 = get_fixture_path('file1.json')
    file2 = get_fixture_path('file2.json')

    expected = read_file('expected.txt').strip()
    result = generate_diff(file1, file2).lower()

    assert result == expected


def test_generate_diff_flat_json_with_format():
    file1 = get_fixture_path('file1.json')
    file2 = get_fixture_path('file2.json')

    expected = read_file('expected.txt').strip()

    result_stylish = generate_diff(file1, file2, 'stylish').lower()
    assert result_stylish == expected


if __name__ == '__main__':
    pytest.main()
