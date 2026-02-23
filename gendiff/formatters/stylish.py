def format_stylish(diff, depth=0):
    indent = '    ' * depth
    lines = ['{']

    for item in diff:
        if item['status'] == 'unchanged':
            lines.append(f"{indent}    {item['key']}: {item['value']}")

        elif item['status'] == 'removed':
            lines.append(f"{indent}  - {item['key']}: {item['value']}")

        elif item['status'] == 'added':
            lines.append(f"{indent}  + {item['key']}: {item['value']}")

        elif item['status'] == 'changed':
            lines.append(f"{indent}  - {item['key']}: {item['old_value']}")
            lines.append(f"{indent}  + {item['key']}: {item['new_value']}")

    lines.append(indent + '}')
    return '\n'.join(lines)
