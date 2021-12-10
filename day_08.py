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
        possibilities = {segment : all_segments.copy() for segment in all_segments} 
        known = {} 
       
        i = 0
        while len(known) < 7:
            i += 1
            if not i % 10: breakpoint()
            for seen_digit in seen_digits:
                # Enumerate the possible digit mappings and remove any segments that aren't used by
                # any digits this one can possibly map to
                possible_digits = [candidate for candidate in normal_digits
                         if len(seen_digit) == len(candidate)
                         and all(candidate & possibilities[segment] for segment in seen_digit)]

                if not possible_digits: breakpoint()

                possible_segments = set.union(*possible_digits)
                for segment in seen_digit:
                    possibilities[segment] &= possible_segments
            
            # if {a,b} must both map to {e,f} in some order
            # then nothing else can map to {e,f}
            # Only need to consider up to size 3 because they'll appear in complementary subsets
            pairs = [(x,y) for x,y in it.combinations(possibilities,2) 
                           if possibilities[x] == possibilities[y] 
                           and len(possibilities[x]) == 2]
            for x,y in pairs:
                vals = possibilities[x]
                for segment in possibilities.keys() - {x,y}:
                    possibilities[segment] -= vals

            unique_segments = (segment for segment in possibilities if len(possibilities[segment]) == 1)
            for segment in unique_segments:
                known[segment] = mit.only(possibilities[segment])

                for other in possibilities.keys() - {segment}:
                    possibilities[other].discard(known[segment])
           
        
        digit_map = {frozenset(comb): {known[s] for s in comb} for comb in combs}
        translated_digits = {frozenset(mit.only(comb for comb in combs if digitmap[comb] == normal[n])) :n for n in range(8)}
        translated_outputs.append(int("".join(translated_digits[o] for o in output)))

    return sum(translated_digits)

