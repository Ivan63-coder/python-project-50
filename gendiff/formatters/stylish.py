import json


def format_value(value, depth=0):
    if isinstance(value, bool):
        return str(value).lower()
    if value is None:
        return 'null'
    if isinstance(value, dict):
        return format_dict(value, depth + 1)
    if isinstance(value, str):
        return value
    return json.dumps(value)


def format_dict(dictionary, depth=0):
    if not dictionary:
        return '{}'

    indent = '    ' * depth
    lines = ['{']

    for key, value in sorted(dictionary.items()):
        formatted_value = format_value(value, depth + 1)
        lines.append(f"{indent}    {key}: {formatted_value}")

    lines.append(f"{indent}}}")
    return '\n'.join(lines)


def format_stylish(diff, depth=0):
    if not diff:
        return '{\n}'

    indent = '    ' * depth
    lines = ['{']

    sorted_diff = sorted(diff, key=lambda x: x['key'])

    for item in sorted_diff:
        key = item['key']

        if item['status'] == 'unchanged':
            formatted_value = format_value(item['value'], depth + 1)
            lines.append(f"{indent}    {key}: {formatted_value}")

        elif item['status'] == 'removed':
            formatted_value = format_value(item['value'], depth + 1)
            lines.append(f"{indent}  - {key}: {formatted_value}")

        elif item['status'] == 'added':
            formatted_value = format_value(item['value'], depth + 1)
            lines.append(f"{indent}  + {key}: {formatted_value}")

        elif item['status'] == 'changed':
            old_value = format_value(item['old_value'], depth + 1)
            new_value = format_value(item['new_value'], depth + 1)
            lines.append(f"{indent}  - {key}: {old_value}")
            lines.append(f"{indent}  + {key}: {new_value}")

    lines.append(f"{indent}}}")
    return '\n'.join(lines)
