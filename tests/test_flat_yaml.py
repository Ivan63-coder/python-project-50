import os
import pytest
from gendiff import generate_diff


def get_fixture_path(filename):
    return os.path.join('tests', 'test_data', 'flat_yaml', filename)


def read_file(filename):
    with open(get_fixture_path(filename), 'r') as f:
        return f.read().strip()


def test_generate_diff_flat_yaml_yml_extension():
    file1 = get_fixture_path('file1.yml')
    file2 = get_fixture_path('file2.yml')

    expected = read_file('expected.txt')
    result = generate_diff(file1, file2)

    assert result == expected


def test_generate_diff_flat_yaml_yaml_extension():
    file1 = get_fixture_path('file1.yaml')
    file2 = get_fixture_path('file2.yaml')

    expected = read_file('expected.txt')
    result = generate_diff(file1, file2)

    assert result == expected


def test_generate_diff_flat_yaml_with_format():
    file1 = get_fixture_path('file1.yml')
    file2 = get_fixture_path('file2.yml')

    expected = read_file('expected.txt')

    result_default = generate_diff(file1, file2)
    assert result_default == expected

    result_stylish = generate_diff(file1, file2, 'stylish')
    assert result_stylish == expected


def test_generate_diff_mixed_json_yaml():
    json_file = os.path.join('tests', 'test_data', 'flat_json', 'file1.json')
    yaml_file = get_fixture_path('file2.yml')

    expected = read_file('expected.txt')
    result = generate_diff(json_file, yaml_file)

    assert result == expected


def test_generate_diff_yaml_with_numbers():
    data1 = """timeout: 50
retries: 3
"""
    data2 = """timeout: 20
retries: 3
"""

    import tempfile
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
        assert result == expected
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

    import tempfile
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
        assert result == expected
    finally:
        os.unlink(file1.name)
        os.unlink(file2.name)


def test_generate_diff_unsupported_format():
    import tempfile
    file1 = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False)
    file1.write("unsupported content")
    file1.close()

    file2 = tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False)
    file2.write("timeout: 20")
    file2.close()

    with pytest.raises(ValueError, match="Unsupported file format"):
        generate_diff(file1.name, file2.name)

    os.unlink(file1.name)
    os.unlink(file2.name)
