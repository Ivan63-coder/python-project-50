def _stringify(value):
    if isinstance(value, dict):
        return '[complex value]'
    elif isinstance(value, bool):
        return str(value).lower()
    elif value is None:
        return 'null'
    elif isinstance(value, str):
        return f"'{value}'"
    elif isinstance(value, (int, float)):
        return str(value)
    else:
        return str(value)


def _format_node(node, path=''):
    current_path = f"{path}.{node['key']}" if path else node['key']
    lines = []

    if node['status'] == 'nested':
        for child in node['children']:
            child_line = _format_node(child, current_path)
            if child_line:
                lines.append(child_line)

    elif node['status'] == 'added':
        value = _stringify(node['value'])
        lines.append(
            f"Property '{current_path}' was added with value: {value}"
            )

    elif node['status'] == 'removed':
        lines.append(f"Property '{current_path}' was removed")

    elif node['status'] == 'changed':
        old_value = _stringify(node['old_value'])
        new_value = _stringify(node['new_value'])
        lines.append(
            f"Property '{current_path}' was updated. "
            f"From {old_value} to {new_value}"
        )
    return '\n'.join(lines)


def format_plain(diff):
    result = []
    for node in diff:
        line = _format_node(node)
        if line:
            result.append(line)
    return '\n'.join(result)
