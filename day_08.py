import itertools as it
import more_itertools as mit
from collections import Counter

def _parse(rawdata):
    parsed = []
    for line in rawdata.splitlines():
        comb, output = line.split("|")
        parsed.append(([set(c) for c in comb.split()], output.split()))
    return parsed

def part_1(*lines):
    r"""
    >>> part_1(*_parse('''\
    ... be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
    ... edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
    ... fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
    ... fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
    ... aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
    ... fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
    ... dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
    ... bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
    ... egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
    ... gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce  
    ... '''))
    26
    """
    outputs = (line[1] for line in lines)
    return sum(len(n) in (2,3,4,7) for output in outputs for n in output)


def part_2(*lines):
    r"""
    >>> part_2(*_parse('''\
    ... acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf
    ... '''))
    5353
    >>> part_2(*_parse('''\
    ... be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
    ... edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
    ... fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
    ... fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
    ... aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
    ... fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
    ... dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
    ... bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
    ... egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
    ... gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce  
    ... '''))
    61229
    """
    translated_outputs = []

    for seen_digits, output in lines:
        digits =  [None] * 10

        digits[1] = mit.only(digit for digit in seen_digits if len(digit) == 2)
        digits[3] = mit.only(digit for digit in seen_digits if len(digit) == 5 and digit > digits[1])
        digits[4] = mit.only(digit for digit in seen_digits if len(digit) == 4)
        digits[7] = mit.only(digit for digit in seen_digits if len(digit) == 3)
        digits[8] = mit.only(digit for digit in seen_digits if len(digit) == 7)

        a = mit.only(digits[7] - digits[1])
        b = mit.only(digits[4] - digits[3])
        e = mit.only(digits[8] - digits[3] - {b})
        g = mit.only(digits[3] - digits[4] - {a})
        d = mit.only(digits[3] - digits[1] - {a, g})
        
        digits[0] = digits[8] - {d}
       
        digits[9] = digits[4] | {a, g}
        digits[6] = mit.only(digit for digit in seen_digits if len(digit) == 6 and digit not in (digits[0], digits[9]))
        c = mit.only(digits[8] - digits[6])
        f = mit.only(digits[1] - {c})
        
        digits[2] = {a,c,d,e,g}
        digits[5] = {a,b,d,f,g}

        translation = {frozenset(digits[n]): str(n) for n in range(10)}
        translated_outputs.append(int("".join(translation[frozenset(o)] for o in output)))

    return sum(translated_outputs)

