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


def format_stylish(diff):
    result = ['{']
    for node in diff:
        node_str = _format_node(node, 1)
        if node_str:
            result.append(node_str)
    result.append('}')
    return '\n'.join(result)


def _stringify(value, depth):
    if isinstance(value, dict):
        indent = '    ' * (depth + 1)
        lines = ['{']
        for key, val in value.items():
            lines.append(f"{indent}{key}: {_stringify(val, depth + 1)}")
        lines.append('    ' * depth + '}')
        return '\n'.join(lines)
    elif isinstance(value, bool):
        return str(value).lower()
    elif value is None:
        return 'null'
    elif isinstance(value, str) and value == '':
        return ''
    elif isinstance(value, str):
        return value
    else:
        return str(value)


def _format_node(node, depth):
    indent = '    ' * depth
    result = []

    if node['status'] == 'nested':
        result.append(f"{indent}{node['key']}: {{")
        for child in node['children']:
            child_str = _format_node(child, depth + 1)
            if child_str:
                result.append(child_str)
        result.append(f"{indent}}}")

    elif node['status'] == 'unchanged':
        value = _stringify(node['value'], depth + 1)
        result.append(f"{indent}    {node['key']}: {value}")

    elif node['status'] == 'removed':
        value = _stringify(node['value'], depth + 1)
        result.append(f"{indent}  - {node['key']}: {value}")

    elif node['status'] == 'added':
        value = _stringify(node['value'], depth + 1)
        result.append(f"{indent}  + {node['key']}: {value}")

    elif node['status'] == 'changed':
        old_value = _stringify(node['old_value'], depth + 1)
        new_value = _stringify(node['new_value'], depth + 1)
        result.append(f"{indent}  - {node['key']}: {old_value}")
        result.append(f"{indent}  + {node['key']}: {new_value}")

    return '\n'.join(result) if result else ''
