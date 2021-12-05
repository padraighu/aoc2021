import pytest
from typing import List, Tuple
from util import read_input

TEST_INPUT, REAL_INPUT = read_input('03')

def parse_input(input: str) -> List[List[int]]:
    return [[int(c) for c in r] for r in input.splitlines()]

def part_one(input: List[List[int]]) -> int:
    res = 0
    ncol = len(input[0])
    nrow = len(input)
    input = [[row[col] for row in input] for col in range(ncol)]
    colsum = [sum(col) for col in input]
    gam = int(''.join(['1' if s > (nrow / 2) else '0' for s in colsum]), 2)
    eps = gam ^ int(f'0b{"1" * ncol}', 2)
    res = gam * eps
    return res

def part_two(input: List[List[int]]) -> int:
    res = 0
    oxy, co2 = part_two_helper(input)
    res = oxy * co2
    return res

def part_two_helper(input: List[List[int]]) -> Tuple[int]:
    ncol = len(input[0])
    cols = [[row[col] for row in input] for col in range(ncol)]
    keep_idx = range(len(input)) # which numbers to keep
    for idx, col in enumerate(cols):
        col = [col[i] for i in keep_idx]
        mc = most_common(col)
        keep_idx = [i for i in keep_idx if cols[idx][i] == mc]
        if len(keep_idx) == 1:
            break
    assert len(keep_idx) == 1
    oxy = int(''.join([str(n) for n in input[keep_idx[0]]]), 2)
    keep_idx = range(len(input)) # which numbers to keep
    for idx, col in enumerate(cols):
        col = [col[i] for i in keep_idx]
        lc = least_common(col)
        keep_idx = [i for i in keep_idx if cols[idx][i] == lc]
        if len(keep_idx) == 1:
            break
    assert len(keep_idx) == 1
    co2 = int(''.join([str(n) for n in input[keep_idx[0]]]), 2)
    return oxy, co2

def most_common(col: List[int]) -> int:
    colsum = sum(col)
    return 1 if colsum >= (len(col) / 2) else 0

def least_common(col: List[int]) -> int:
    return 1 if most_common(col) == 0 else 0

@pytest.mark.parametrize('input, res', [(TEST_INPUT, 198), (REAL_INPUT, 3912944)])
def test_part_one(input: str, res: int) -> None:
    assert part_one(parse_input(input)) == res

@pytest.mark.parametrize('input, res', [(TEST_INPUT, 230), (REAL_INPUT, 4996233)])
def test_part_two(input: str, res: int) -> None:
    assert part_two(parse_input(input)) == res
