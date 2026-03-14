from gendiff.diff_builder import build_diff
from gendiff.formatters.stylish import format_stylish
from gendiff.parser import parse_file


def generate_diff(file_path1, file_path2, format_name='stylish'):
    data1 = parse_file(file_path1)
    data2 = parse_file(file_path2)

    diff = build_diff(data1, data2)

    if format_name == 'stylish':
        return format_stylish(diff)
    else:
        return format_stylish(diff)
