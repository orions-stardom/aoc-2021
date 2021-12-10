import itertools as it
import more_itertools as mit
from collections import Counter

def _parse(rawdata):
    parsed = []
    for line in rawdata.splitlines():
        comb, output = line.split("|")
        parsed.append((set(c for c in comb.split()), output.split()))
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
    5353 
    """
    normal_digits = [set("abcefg"), 
                     set("cf"),
                     set("acdeg"),
                     set("acdfg"),
                     set("bcdf"),
                     set("abdfg"),
                     set("abdefg"),
                     set("acf"),
                     set("abcdefg"),
                     set("abcdfg"),
                    ]
    all_segments = normal_digits[8]
    
    translated_outputs = []
    for seen_digits, output in lines:
        possibilities = {segment : all_segments.copy() for segment in all_segments} # seen : real
        
        for i, seen_digit in enumerate(it.cycle(seen_digits)):
            possible_digits = (candidate for candidate in normal_digits
                     if len(seen_digit) == len(candidate)
                     and all(candidate & possibilities[segment] for segment in seen_digit))

            possible_segments = set.union(*possible_digits)
            for segment in seen_digit:
                possibilities[segment] &= possible_segments

            if all(len(m) == 1 for m in possibilities.values()):
                break

            if not all(possibilities.values()): breakpoint()
            
            if i and not i % 20:
                breakpoint()
        
        segment_map = {seen:possible.pop() for seen, possible in possibilities.items()}
        digit_map = {frozenset(comb): {segment_map[s] for s in comb} for comb in combs}
        translated_digits = {frozenset(mit.only(comb for comb in combs if digitmap[comb] == normal[n])) :n for n in range(8)}
        translated_outputs.append(int("".join(translated_digits[o] for o in output)))

    return sum(translated_digits)

