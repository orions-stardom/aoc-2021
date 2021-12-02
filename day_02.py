from parse import parse

def part_1(data):
    r"""
    >>> part_1('''\
    ... forward 5
    ... down 5
    ... forward 8
    ... up 3
    ... down 8
    ... forward 2''')
    150

    """
    horiz, depth = (0, 0)

    for line in data.splitlines():
        direction, amount = parse("{} {:n}", line)

        if direction == "forward":
            horiz += amount
        elif direction == "down":
            depth += amount
        elif direction == "up":
            depth -= amount
    return horiz * depth

def part_2(data):
    r"""
    >>> part_2('''\
    ... forward 5
    ... down 5
    ... forward 8
    ... up 3
    ... down 8
    ... forward 2''')
    900

    """

    horiz, depth, aim = (0, 0, 0)

    for line in data.splitlines():
        direction, amount = parse("{} {:n}", line)

        if direction == "forward":
            horiz += amount
            depth += aim * amount
        elif direction == "down":
            aim += amount
        elif direction == "up":
            aim -= amount

    return horiz * depth
