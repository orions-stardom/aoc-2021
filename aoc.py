#! /usr/bin/env python
import argparse
from datetime import date
import doctest
import importlib
import sys

import aocd

year = 2021

parser = argparse.ArgumentParser()
parser.add_argument("--skip-test", action="store_true", help="Skip automated doc test when running. When omitted, the entire module for the selected day is tested even if only one part would actually be run")
parser.add_argument("--submit", action="store_false")
parser.add_argument("--day", type=int, choices=range(1,26), help="Omit for today but only during the advent season")
parser.add_argument("--part", type=int, choices=[1,2], action="append", help="Which puzzle(s) to run. If omitted, run all that exist in the script for the selected day")

args = parser.parse_args()

if args.day is None: 
    today = date.today()
    if (today.month, today.year) != (12, year) or not 1 <= today.day <= 25:
        sys.exit(f"Can only guess the day during AOC season {year}")

    args.day = today.day

solution_module = importlib.import_module(f'day_{args.day:02}')

if not args.skip_test:
    failure, tests = doctest.testmod(solution_module)
    if failure > 0:
        sys.exit(f"Failed {failure}/{tests} tests")

data = aocd.get_data(year=year, day=args.day)
for part in (args.part or [1,2]):
    try:
        solution = getattr(solution_module, f'part_{part}')(data)
    except AttributeError:
        # If parts were specified, they must exist, but if we're running all of them 
        if args.part:
            sys.exit(f"Day {args.day} has no solution for part {part}")
        else:
            breakpoint()

    print(f"Solution to part {part}: ", solution, sep="\n")

    if args.submit:
        # aocd uses parts a and b for some reason, even though AOC uses parts One and Two
        aocd.submit(solution, year=year, day=args.day, part='ab'[part-1], reopen=False)

