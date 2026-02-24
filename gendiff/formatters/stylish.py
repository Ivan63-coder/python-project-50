def format_value(value, depth):
    if isinstance(value, bool):
        return str(value).lower()
    if value is None:
        return 'null'
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, dict):
        indent = '    ' * (depth + 1)
        lines = ['{']
        for key, val in value.items():
            lines.append(f"{indent}{key}: {format_value(val, depth + 1)}")
        lines.append('    ' * depth + '}')
        return '\n'.join(lines)
    return str(value)


def format_stylish(diff, depth=0):
    indent = '    ' * depth
    lines = ['{']

    sorted_diff = sorted(diff, key=lambda x: x['key'])

    for item in sorted_diff:
        key = item['key']

        if item['status'] == 'unchanged':
            value = format_value(item['value'], depth + 1)
            lines.append(f"{indent}    {key}: {value}")

        elif item['status'] == 'removed':
            value = format_value(item['value'], depth + 1)
            lines.append(f"{indent}  - {key}: {value}")

        elif item['status'] == 'added':
            value = format_value(item['value'], depth + 1)
            lines.append(f"{indent}  + {key}: {value}")

        elif item['status'] == 'changed':
            old_value = format_value(item['old_value'], depth + 1)
            new_value = format_value(item['new_value'], depth + 1)
            lines.append(f"{indent}  - {key}: {old_value}")
            lines.append(f"{indent}  + {key}: {new_value}")

    lines.append(indent + '}')
    return '\n'.join(lines)
