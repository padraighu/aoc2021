from typing import List

import pytest
from util import read_input

TEST_INPUT, REAL_INPUT = read_input("01")


def parse_input(input: str) -> List[int]:
    return [int(i) for i in input.splitlines()]


def part_one(input: List[int]) -> int:
    res = 0
    for curr, prev in zip(input[1:], input):
        if curr > prev:
            res += 1
    return res


def part_two(input: List[int]) -> int:
    res = 0
    curr = 0
    prev = None
    for a, b, c in zip(input, input[1:], input[2:]):
        curr = a + b + c
        if prev and curr > prev:
            res += 1
        prev = curr
    return res


@pytest.mark.parametrize("input, res", [(TEST_INPUT, 7), (REAL_INPUT, 1752)])
def test_part_one(input: str, res: int) -> None:
    assert part_one(parse_input(input)) == res


@pytest.mark.parametrize("input, res", [(TEST_INPUT, 5), (REAL_INPUT, 1781)])
def test_part_two(input: str, res: int) -> None:
    assert part_two(parse_input(input)) == res
