import os

import pytest

from gendiff.generate_diff import generate_diff


def get_fixture_path(extension, filename):
    return os.path.join('tests', 'test_data', f'nested_{extension}', filename)


def read_file(extension, filename):
    with open(get_fixture_path(extension, filename), 'r') as f:
        return f.read()


@pytest.mark.parametrize("extension", ['json', 'yaml'])
def test_generate_diff_nested(extension):
    file1 = get_fixture_path(extension, f'file1.{extension}')
    file2 = get_fixture_path(extension, f'file2.{extension}')

    expected = read_file('json', 'expected.txt').strip()
    result = generate_diff(file1, file2)

    assert result == expected


@pytest.mark.parametrize("extension", ['json', 'yaml'])
def test_generate_diff_nested_with_format(extension):
    file1 = get_fixture_path(extension, f'file1.{extension}')
    file2 = get_fixture_path(extension, f'file2.{extension}')

    expected = read_file('json', 'expected.txt').strip()

    result_default = generate_diff(file1, file2)
    assert result_default == expected

    result_stylish = generate_diff(file1, file2, 'stylish')
    assert result_stylish == expected
