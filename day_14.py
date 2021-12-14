import more_itertools as mit
from collections import Counter

def _parse(rawdata):
    start, rulesdata = rawdata.split("\n\n")
    rules = dict(line.split(" -> ") for line in rulesdata.splitlines())
    return start, rules


def part_1(start, rules):
    r"""
    >>> part_1(*_parse('''\
    ... NNCB
    ... 
    ... CH -> B
    ... HH -> N
    ... CB -> H
    ... NH -> C
    ... HB -> C
    ... HC -> B
    ... HN -> C
    ... NN -> C
    ... BH -> H
    ... NC -> B
    ... NB -> B
    ... BN -> B
    ... BB -> N
    ... BC -> B
    ... CC -> N
    ... CN -> C
    ... '''))
    1588
    """
    def nextstate(state, rules):
        (head,), state = mit.spy(state)
        yield head
        for l,r in mit.pairwise(state):
            pair = f"{l}{r}"
            if pair in rules:
                yield rules[pair]

            yield r
    
    state = start
    for _ in range(10):
        state = nextstate(state, rules)

    count = Counter(state).most_common()
    return count[0][1] - count[-1][1]

def part_2(start, rules):
    r"""
    >>> part_2(*_parse('''\
    ... NNCB
    ... 
    ... CH -> B
    ... HH -> N
    ... CB -> H
    ... NH -> C
    ... HB -> C
    ... HC -> B
    ... HN -> C
    ... NN -> C
    ... BH -> H
    ... NC -> B
    ... NB -> B
    ... BN -> B
    ... BB -> N
    ... BC -> B
    ... CC -> N
    ... CN -> C
    ... '''))
    2188189693529
    """
    state = Counter(f"{l}{r}" for l,r in mit.pairwise(start)) 
    for _ in range(40):
        newstate = Counter()
        for pair, count in state.items():
            if pair in rules:
                l,r = pair
                c = rules[pair]
                newstate.update({f"{l}{c}": count, f"{c}{r}":count})
            else:
                newstate[pair] = count

        state = newstate

    # Convert back from counting pairs to counting individual elements
    # because the pairs overlap, we only want to count the lhs of each
    # but then we haven't counted the tail element.. but it won't ever 
    # have changed
    count = Counter(start[-1])
    for (l,r), n in state.items():
        count.update({l:n})

    count = count.most_common()
    return count[0][1] - count[-1][1]
