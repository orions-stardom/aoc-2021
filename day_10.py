import statistics

def _parse(rawdata):
    return rawdata.splitlines() 

def part_1(*lines):
    r"""
    >>> part_1(*_parse('''\
    ... [({(<(())[]>[[{[]{<()<>>
    ... [(()[<>])]({[<{<<[]>>(
    ... {([(<{}[<>[]}>{[]{[(<()>
    ... (((({<>}<{<{<>}{[]{[]{}
    ... [[<[([]))<([[{}[[()]]]
    ... [{[{({}]{}}([{[{{{}}([]
    ... {<[[]]>}<{[{[{[]{()[[[]
    ... [<(<(<(<{}))><([]([]()
    ... <{([([[(<>()){}]>(<<{{
    ... <{([{{}}[<[[[<>{}]]]>[]]
    ... '''))
    26397
    """
    expect = {"(":")", "{":"}", "<":">", "[":"]"}

    def score(line):
        stack = []
        points = {")": 3, "]": 57, "}": 1197, ">": 25137}
        for char in line:
            if char in expect:
                stack.append(char)
                continue
           
            need = expect[stack.pop()]
            if char != need:
                return points[char]
        
        # not corrupt
        return 0
    return sum(score(line) for line in lines)


def part_2(*lines):
    r"""
    >>> part_2(*_parse('''\
    ... [({(<(())[]>[[{[]{<()<>>
    ... [(()[<>])]({[<{<<[]>>(
    ... {([(<{}[<>[]}>{[]{[(<()>
    ... (((({<>}<{<{<>}{[]{[]{}
    ... [[<[([]))<([[{}[[()]]]
    ... [{[{({}]{}}([{[{{{}}([]
    ... {<[[]]>}<{[{[{[]{()[[[]
    ... [<(<(<(<{}))><([]([]()
    ... <{([([[(<>()){}]>(<<{{
    ... <{([{{}}[<[[[<>{}]]]>[]]
    ... '''))
    288957
    """
    expect = {"(":")", "{":"}", "<":">", "[":"]"}
  
    def score(line):
        stack = []
        for char in line:
            if char in expect:
                stack.append(char)
                continue
           
            need = expect[stack.pop()]
            if char != need:
                # Corrupt, doesnt count 
                return None       
       
        points = {")": 1, "]": 2, "}": 3, ">": 4}
        total = 0
        while stack:
            total *= 5
            total += points[expect[stack.pop()]]
        return total

    return statistics.median(s for s in map(score, lines) if s is not None)
