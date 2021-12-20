import itertools as it

class Image:
    @classmethod
    def parse(cls, data):
        data = data.splitlines()
        pixels = set()
        xs, ys = range(len(data[0])), range(len(data))
        for x,y in it.product(xs,ys):
            if data[y][x] == "#":
                pixels.add((x,y))

        return cls(pixels, False)

    def __init__(self, pixels, default):
        self.pixels = pixels
        self.default = default

        self.xmin, self.xmax, self.ymin, self.ymax = (
            min(c[0] for c in self.pixels),
            max(c[0] for c in self.pixels),
            min(c[1] for c in self.pixels),
            max(c[1] for c in self.pixels),
        )

    def neighbourhood(self, x,y):
        return (self[x-1, y-1] * 2**8 + 
                self[x  , y-1] * 2**7 +
                self[x+1, y-1] * 2**6 +
                self[x-1, y  ] * 2**5 +
                self[x  , y  ] * 2**4 +
                self[x+1, y  ] * 2**3 +
                self[x-1, y+1] * 2**2 +
                self[x  , y+1] * 2**1 +
                self[x+1, y+1] * 2**0)

    def __getitem__(self, item):
        x,y = item
        if self.xmin <= x <= self.xmax and self.ymin <= y <= self.ymax:
            return item in self.pixels

        return self.default

    def enhance(self, algo):
        enhanced = set()
        # Need to consider every pixel whose neighbourhood overlaps with our 
        # stored boundaries
        xs = range(self.xmin-2,self.xmax+3)
        ys = range(self.ymin-2,self.ymax+3)

        enhanced = {(x,y) for x,y in it.product(xs, ys) if algo[self.neighbourhood(x,y)] == "#"}
        default = int(f"0b{str(int(self.default)) * 9}", 2)
        return Image(enhanced, algo[default] == "#")

    def __str__(self):
        xs = range(self.xmin, self.xmax + 1)
        ys = range(self.ymin, self.ymax + 1)
        return "\n".join("".join("#" if self[x,y] else "." for x in xs) for y in ys)

def _parse(rawdata):
    algo, imagedata = rawdata.split("\n\n")
    return algo.replace("\n", ""), Image.parse(imagedata)

def part_1(algo, image):
    r"""
    >>> part_1(*_parse('''\
    ... ..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..##
    ... #..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###
    ... .######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#.
    ... .#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#.....
    ... .#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#..
    ... ...####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.....
    ... ..##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#
    ... 
    ... #..#.
    ... #....
    ... ##..#
    ... ..#..
    ... ..###
    ... '''))
    35

    """
    return len(image.enhance(algo).enhance(algo).pixels)

def part_2(algo, image):
    r"""
    >>> part_2(*_parse('''\
    ... ..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..##
    ... #..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###
    ... .######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#.
    ... .#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#.....
    ... .#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#..
    ... ...####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.....
    ... ..##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#
    ... 
    ... #..#.
    ... #....
    ... ##..#
    ... ..#..
    ... ..###
    ... '''))
    3351

    """
    for _ in range(50):
        image = image.enhance(algo)

    return len(image.pixels)
