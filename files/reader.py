import os


def get_puzzle_input_path(dirname: str):
    return os.path.join(dirname, 'puzzle_input.txt')


def split_grouped_input(input):
    unparse_passports = []
    current = []
    for line in input.splitlines():
        if len(line) > 0:
            current.append(line.strip())
        else:
            if len(current) == 0:
                pass
            else:
                unparse_passports.append(current)
                current = []

    if len(current) > 0:
        unparse_passports.append(current)

    return [" ".join(x).strip() for x in unparse_passports]
