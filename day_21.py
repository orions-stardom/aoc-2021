from parse import parse
import itertools as it
import more_itertools as mit
from copy import deepcopy
from collections import Counter
from typing import NamedTuple

class Player(NamedTuple):
    pos: int = 1
    score: int = 0

    def move(self, totalroll):
        pos=((self.pos-1 + totalroll) % 10)+1
        score=self.score + pos
        return Player(pos, score)

def _parse(rawdata):
    return [Player(parse("Player {} starting position: {:n}", line)[1]) for line in rawdata.splitlines()]

def part_1(*players):
    r"""
    >>> part_1(*_parse('''\
    ... Player 1 starting position: 4
    ... Player 2 starting position: 8
    ... '''))
    739785

    """
    dice = it.cycle(range(1,101))
    players = list(players)
    for round, roll in enumerate(mit.chunked(dice, 3)):
        player = round % len(players)
        players[player] = players[player].move(sum(roll))
        if players[player].score >= 1000:
            break

    rolls = (round+1)*3
    return min(p.score for p in players)*rolls

def part_2(*players):
    r"""
    >>> part_2(*_parse('''\
    ... Player 1 starting position: 4
    ... Player 2 starting position: 8
    ... '''))
    444356092776315

    """
    overall_score = [0] * len(players)
    possible_rolls = Counter(map(sum,it.product((1,2,3), repeat=3)))

    multiverse = Counter([players])
    for round in it.count():
        if not multiverse:
            break
        
        current_player = round % len(players)
        new_multiverse = Counter()
        
        for universe, nuniverses in multiverse.items():
            for roll, nrolls in possible_rolls.items():
                spawncount = nuniverses*nrolls
                players = list(universe)
                players[current_player] = players[current_player].move(roll)

                if players[current_player].score >= 21:
                    overall_score[current_player] += spawncount
                else:
                    new_multiverse[tuple(players)] += spawncount
        
        multiverse = new_multiverse
    return max(overall_score)
