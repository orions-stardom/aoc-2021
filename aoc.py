#! /usr/bin/env python
import argparse
from datetime import date
import doctest
import importlib
import sys

import aocd

import dotenv; dotenv.load_dotenv()

year = 2021

parser = argparse.ArgumentParser()
parser.add_argument("--skip-test", action="store_true", help="Skip automated doc test when running")
parser.add_argument("--submit", action="store_false")
parser.add_argument("--day", type=int, choices=range(1,26), help="Omit for today but only during the advent season")
parser.add_argument("--part", type=int, choices=[1,2])

args = parser.parse_args()

if args.day is None: 
    today = date.today()
    if (today.month, today.year) != (12, year) or not 1 <= today.day <= 25:
        sys.exit(f"Can only guess the day during AOC season {year}")

    args.day = today.day

solution_module = importlib.import_module(f'day_{args.day:02}')

if args.part is None:
    args.part = 2 if hasattr(solution_module, 'part_2') else 1

if not args.skip_test:
    failure, tests = doctest.testmod(solution_module)
    if failure > 0:
        sys.exit(f"Failed {failure}/{tests} tests")

data = aocd.get_data(year=year, day=args.day)
solution = getattr(solution_module, f'part_{args.part}')(data)
print("Solution: ", solution, sep="\n")

if args.submit:
    aocd.submit(solution, year=year, day=args.day, part='ab'[args.part-1], reopen=False)

