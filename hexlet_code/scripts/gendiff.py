import argparse
import json


def read_file(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)


def generate_diff(file_path1, file_path2, format_name='stylish'):
    data1 = read_file(file_path1)
    data2 = read_file(file_path2)

    return (f"File 1 ({file_path1}): {len(data1)} keys\n"
            f"File 2 ({file_path2}): {len(data2)} keys\n"
            f"Format: {format_name}\n"
            f"Will compare {list(data1.keys())} with {list(data2.keys())}")


def main():
    parser = argparse.ArgumentParser(
        description='Compares two configuration files and shows a difference.',
        usage='gendiff [-h] [-f FORMAT] first_file second_file'
    )

    parser.add_argument(
        'first_file',
    )

    parser.add_argument(
        'second_file',
    )

    parser.add_argument(
        '-f', '--format',
        default='stylish',
        help='set format of output (default: stylish)',
    )

    args = parser.parse_args()

    result = generate_diff(args.first_file, args.second_file, args.format)
    print(result)


if __name__ == '__main__':
    main()
