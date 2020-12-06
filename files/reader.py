import os


def get_puzzle_input_path(dirname: str):
    return os.path.join(dirname, 'puzzle_input.txt')


def split_groups(input: str):
    groups = []
    current = []
    for line in input.splitlines():
        if len(line) > 0:
            current.append(line.strip())
        else:
            if len(current) == 0:
                pass
            else:
                groups.append(current)
                current = []

    if len(current) > 0:
        groups.append(current)

    return groups


def split_grouped_input(input: str):
    return [" ".join(x).strip() for x in split_groups(input)]
