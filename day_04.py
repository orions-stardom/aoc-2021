import numpy as np
import numpy.ma as ma

import more_itertools as mit

class Board:
    def __init__(self, data):
        self.board = ma.array([[int(i) for i in line.split()] for line in data])

    @property
    def has_won(self):
        return np.any(self.board.mask) and (np.any(np.all(self.board.mask, axis=0)) or np.any(np.all(self.board.mask, axis=1)))
    
    @property
    def sum(self):
        return self.board.sum()

    def call(self, num):
        self.board[self.board == num] = ma.masked

def part_1(data):
    r"""
    >>> part_1('''\
    ... 7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1
    ... 
    ... 22 13 17 11  0
    ...  8  2 23  4 24
    ... 21  9 14 16  7
    ...  6 10  3 18  5
    ...  1 12 20 15 19
    ...
    ...  3 15  0  2 22
    ...  9 18 13 17  5
    ... 19  8  7 25 23
    ... 20 11 10 24  4
    ... 14 21 16 12  6
    ...
    ... 14 21 17 24  4
    ... 10 16 15  9 19
    ... 18  8 23 26 20
    ... 22 11 13  6  5
    ...  2  0 12  3  7''')
    4512
    """

    data = data.splitlines()
    nums = [int(n) for n in data[0].split(",")]

    boards = [Board(chunk[1:]) for chunk in mit.chunked(data[1:], 6)]
   
    for num in nums:
        for board in boards:
            board.call(num)
            if board.has_won:
                return num * board.sum

def part_2(data):
    r"""
    >>> part_2('''\
    ... 7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1
    ... 
    ... 22 13 17 11  0
    ...  8  2 23  4 24
    ... 21  9 14 16  7
    ...  6 10  3 18  5
    ...  1 12 20 15 19
    ...
    ...  3 15  0  2 22
    ...  9 18 13 17  5
    ... 19  8  7 25 23
    ... 20 11 10 24  4
    ... 14 21 16 12  6
    ...
    ... 14 21 17 24  4
    ... 10 16 15  9 19
    ... 18  8 23 26 20
    ... 22 11 13  6  5
    ...  2  0 12  3  7''')
    1924
    """
    data = data.splitlines()
    nums = [int(n) for n in data[0].split(",")]

    boards = [Board(chunk[1:]) for chunk in mit.chunked(data[1:], 6)]
    for num in nums:
        for board in boards:
            board.call(num)
       
        if len(boards) > 1:
            boards = [board for board in boards if not board.has_won]
        elif boards[0].has_won:
            return num * boards[0].sum

