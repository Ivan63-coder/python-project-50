import os
import tempfile

from gendiff.generate_diff import generate_diff


def get_fixture_path(filename):
    return os.path.join('tests', 'test_data', 'flat_yaml', filename)


def read_file(filename):
    with open(get_fixture_path(filename), 'r') as f:
        return f.read().strip()


def normalize_output(text):
    return [line.rstrip() for line in text.split('\n') if line.rstrip()]


def test_generate_diff_flat_yaml_yml_extension():
    file1 = get_fixture_path('file1.yml')
    file2 = get_fixture_path('file2.yml')

    expected = read_file('expected.txt')
    result = generate_diff(file1, file2)

    result_lines = normalize_output(result)
    expected_lines = normalize_output(expected)

    assert result_lines == expected_lines


def test_generate_diff_flat_yaml_yaml_extension():
    file1 = get_fixture_path('file1.yaml')
    file2 = get_fixture_path('file2.yaml')

    expected = read_file('expected.txt')
    result = generate_diff(file1, file2)

    result_lines = normalize_output(result)
    expected_lines = normalize_output(expected)

    assert result_lines == expected_lines


def test_generate_diff_flat_yaml_with_format():
    file1 = get_fixture_path('file1.yml')
    file2 = get_fixture_path('file2.yml')

    expected = read_file('expected.txt')

    result_default = generate_diff(file1, file2)
    result_default_lines = normalize_output(result_default)
    expected_lines = normalize_output(expected)
    assert result_default_lines == expected_lines

    result_stylish = generate_diff(file1, file2, 'stylish')
    result_stylish_lines = normalize_output(result_stylish)
    assert result_stylish_lines == expected_lines


def test_generate_diff_mixed_json_yaml():
    json_file = os.path.join('tests', 'test_data', 'flat_json', 'file1.json')
    yaml_file = get_fixture_path('file2.yml')

    expected = read_file('expected.txt')
    result = generate_diff(json_file, yaml_file)

    result_lines = normalize_output(result)
    expected_lines = normalize_output(expected)
    assert result_lines == expected_lines


def test_generate_diff_yaml_with_numbers():
    data1 = """timeout: 50
retries: 3
"""
    data2 = """timeout: 20
retries: 3
"""

    file1 = tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False)
    file1.write(data1)
    file1.close()

    file2 = tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False)
    file2.write(data2)
    file2.close()

    expected = """{
        retries: 3
    - timeout: 50
    + timeout: 20
}"""

    try:
        result = generate_diff(file1.name, file2.name)
        result_lines = normalize_output(result)
        expected_lines = normalize_output(expected)
        assert result_lines == expected_lines
    finally:
        os.unlink(file1.name)
        os.unlink(file2.name)


def test_generate_diff_yaml_with_boolean():
    data1 = """follow: true
verbose: false
"""
    data2 = """follow: false
verbose: false
"""

    file1 = tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False)
    file1.write(data1)
    file1.close()

    file2 = tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False)
    file2.write(data2)
    file2.close()

    expected = """{
    - follow: true
    + follow: false
        verbose: false
}"""

    try:
        result = generate_diff(file1.name, file2.name)
        result_lines = normalize_output(result)
        expected_lines = normalize_output(expected)
        assert result_lines == expected_lines
    finally:
        os.unlink(file1.name)
        os.unlink(file2.name)


def test_generate_diff_yaml_with_null():
    data1 = """value: null
"""
    data2 = """value: not_null
"""

    file1 = tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False)
    file1.write(data1)
    file1.close()

    file2 = tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False)
    file2.write(data2)
    file2.close()

    expected = """{
    - value: null
    + value: not_null
}"""

    try:
        result = generate_diff(file1.name, file2.name)
        result_lines = normalize_output(result)
        expected_lines = normalize_output(expected)
        assert result_lines == expected_lines
    finally:
        os.unlink(file1.name)
        os.unlink(file2.name)
