import os
import pytest
from gendiff import generate_diff


def get_fixture_path(filename):
    return os.path.join('tests', 'test_data', 'flat_json', filename)


def read_file(filename):
    with open(get_fixture_path(filename), 'r') as f:
        return f.read().strip()


def test_generate_diff_flat_json():
    file1 = get_fixture_path('file1.json')
    file2 = get_fixture_path('file2.json')

    expected = read_file('expected.txt')
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

    assert result == expected


def test_generate_diff_flat_json_with_format():
    """Test generate_diff with specified format."""
    file1 = get_fixture_path('file1.json')
    file2 = get_fixture_path('file2.json')

    expected = read_file('expected.txt')

    result_default = generate_diff(file1, file2)
    assert result_default == expected

    result_stylish = generate_diff(file1, file2, 'stylish')
    assert result_stylish == expected


if __name__ == '__main__':
    pytest.main()
