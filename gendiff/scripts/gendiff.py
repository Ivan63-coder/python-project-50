import argparse


def generate_diff(file_path1, file_path2, format_name='stylish'):
    return f"Comparing {file_path1} and {file_path2} in {format_name} format"


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
        help='set format of output',
    )

    args = parser.parse_args()

    result = generate_diff(args.first_file, args.second_file, args.format)
    print(result)


if __name__ == '__main__':
    main()
