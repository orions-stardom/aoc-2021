import itertools as it
import more_itertools as mit

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
    #breakpoint()
    return sum(len(n) in (2,3,4,7) for output in outputs for n in output)


def part_2(*lines):
    r"""
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
    normal = [set("abcefg"), set("cf"), set("acdeg"), set("acdfg"), set("bcdf"), set("abdfg"), set("abdefg"), set("acf"), set("abcdefg"), set("abcdfg")]
    universalset = normal[8]
    
    translated_outputs = []
    for combs, output in lines:
        possibilities = {segment : universalset.copy() for segment in universalset }

        for consider in it.cycle(combs):
            cands = {frozenset(cand) for cand in normal if len(consider) == len(cand)}
            cand_segments = set(it.chain.from_iterable(cands))
             
            for eliminate in it.product((universalset - cands), consider):
                possibilities[eliminate[0]].discard(eliminate[1])

            if all(len(m) == 1 for m in possibilities.values()):
                break
        
        # possibilities are what normal segment can map to which mixed up segement
        # but now we need it the other way around
        segment_map = {l2.pop():l1 for l1,l2 in possibilities.items()}
        breakpoint()
        digit_map = {frozenset(comb): {segment_map[s] for s in comb} for comb in combs}
        translated_digits = {frozenset(mit.only(comb for comb in combs if digitmap[comb] == normal[n])) :n for n in range(8)}
        translated_outputs.append(int("".join(translated_digits[o] for o in output)))

    return sum(translated_digits)

