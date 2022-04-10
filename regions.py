
def get_regions():
    with open('regions.txt') as f:
        lines = [line.strip() for line in f.readlines()]

    return lines

