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


def build_diff(data1, data2):
    all_keys = sorted(set(data1.keys()) | set(data2.keys()))
    diff = []

    for key in all_keys:
        if key not in data1:
            diff.append({
                'key': key,
                'status': 'added',
                'value': data2[key]
            })
        elif key not in data2:
            diff.append({
                'key': key,
                'status': 'removed',
                'value': data1[key]
            })
        elif data1[key] == data2[key]:
            diff.append({
                'key': key,
                'status': 'unchanged',
                'value': data1[key]
            })
        else:
            diff.append({
                'key': key,
                'status': 'changed',
                'old_value': data1[key],
                'new_value': data2[key]
            })
    return diff
