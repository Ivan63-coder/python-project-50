def _stringify(value, depth):
    if isinstance(value, dict):
        indent = ' ' * (depth * 4)
        lines = ['{']
        for key, val in value.items():
            lines.append(f"{indent}{key}: {_stringify(val, depth + 1)}")
        lines.append(' ' * ((depth - 1) * 4) + '}')
        return '\n'.join(lines)
    elif isinstance(value, bool):
        return str(value).lower()
    elif value is None:
        return 'null'
    elif isinstance(value, str):
        return value
    else:
        return str(value)


def _format_node(node, depth):
    indent = ' ' * (depth * 4 - 2)
    result = []

    if node['status'] == 'nested':
        result.append(f"{indent}{node['key']}: {{")
        for child in node['children']:
            child_lines = _format_node(child, depth + 1)
            if child_lines:
                result.append(child_lines)
        result.append(f"{indent}}}")

    elif node['status'] == 'unchanged':
        value = _stringify(node['value'], depth + 1)
        result.append(f"{indent}  {node['key']}: {value}")

    elif node['status'] == 'removed':
        value = _stringify(node['value'], depth + 1)
        result.append(f"{indent}- {node['key']}: {value}")

    elif node['status'] == 'added':
        value = _stringify(node['value'], depth + 1)
        result.append(f"{indent}+ {node['key']}: {value}")

    elif node['status'] == 'changed':
        old_value = _stringify(node['old_value'], depth + 1)
        new_value = _stringify(node['new_value'], depth + 1)
        result.append(f"{indent}- {node['key']}: {old_value}")
        result.append(f"{indent}+ {node['key']}: {new_value}")

    return '\n'.join(result) if result else ''


def format_stylish(diff):
    result = ['{']
    for node in diff:
        node_str = _format_node(node, 1)
        if node_str:
            result.append(node_str)
    result.append('}')
    return '\n'.join(result)
