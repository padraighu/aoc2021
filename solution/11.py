from collections import deque
from typing import Deque, List, Set, Tuple
import itertools

import pytest
from util import read_input

TEST_INPUT, REAL_INPUT = read_input("11")


def parse_input(input: str) -> List[List[int]]:
    return [[int(v) for v in l] for l in input.splitlines()]


def part_one(octs: List[List[int]]) -> int:
    res = 0
    STEPS = 100
    deltas = list(itertools.product([1, 0, -1], [-1, 0, 1]))
    nrow = len(octs)
    ncol = len(octs[0])
    for _step in range(STEPS):
        # initialize with all points in matrix
        stack = list(itertools.product(range(nrow), range(ncol)))
        flashed = set()  # type: Set[Tuple[int, int]]
        while len(stack) > 0:
            i, j = stack.pop()
            if (i, j) not in flashed:
                octs[i][j] += 1
                if octs[i][j] > 9:
                    res += 1
                    octs[i][j] = 0
                    flashed.add((i, j))
                    nbrs = [(i+x,j+y) for (x, y) in deltas if 0 <= i+x < nrow and 0 <= j+y < ncol and (x, y) != (0,0)]
                    stack += nbrs
    return res

def part_two(octs: List[List[int]]) -> int:
    res = 0
    deltas = list(itertools.product([1, 0, -1], [-1, 0, 1]))
    nrow = len(octs)
    ncol = len(octs[0])
    step = 0
    while True:
        step += 1
        # initialize with all points in matrix
        stack = list(itertools.product(range(nrow), range(ncol)))
        flashed = set()  # type: Set[Tuple[int, int]]
        while len(stack) > 0:
            i, j = stack.pop()
            if (i, j) not in flashed:
                octs[i][j] += 1
                if octs[i][j] > 9:
                    octs[i][j] = 0
                    flashed.add((i, j))
                    nbrs = [(i+x,j+y) for (x, y) in deltas if 0 <= i+x < nrow and 0 <= j+y < ncol and (x, y) != (0,0)]
                    stack += nbrs
        sync = True
        for i in range(nrow):
            for j in range(ncol):
                if octs[i][j] != 0:
                    sync = False
                    break
        if sync:
            res = step
            break
    return res

@pytest.mark.parametrize("input, res", [(TEST_INPUT, 1656), (REAL_INPUT, 1642)])
def test_part_one(input: str, res: int) -> None:
    assert part_one(parse_input(input)) == res

@pytest.mark.parametrize("input, res", [(TEST_INPUT, 195), (REAL_INPUT, 320)])
def test_part_two(input: str, res: int) -> None:
    assert part_two(parse_input(input)) == res