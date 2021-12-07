from collections import defaultdict
from typing import List

import pytest
from util import read_input

TEST_INPUT, REAL_INPUT = read_input("07")


def parse_input(input: str) -> List[int]:
    return [int(l) for l in input.split(",")]


def part_one(crabs: List[int]) -> int:
    res = 99999999999
    for center in range(min(crabs), max(crabs)):
        fuel = 0
        for crab in crabs:
            fuel += abs(crab-center)
        if fuel < res:
            res = fuel
    return res


def part_two(crabs: List[int]) -> int:
    res = 99999999999
    for center in range(min(crabs), max(crabs)):
        fuel = 0
        for crab in crabs:
            n = abs(crab-center) 
            fuel += int(n * (n+1) / 2)
        if fuel < res:
            res = fuel
    return res

@pytest.mark.parametrize("input, res", [(TEST_INPUT, 37), (REAL_INPUT, 343441)])
def test_part_one(input: str, res: int) -> None:
    assert part_one(parse_input(input)) == res


@pytest.mark.parametrize("input, res", [(TEST_INPUT, 168), (REAL_INPUT, 98925151)])
def test_part_two(input: str, res: int) -> None:
    assert part_two(parse_input(input)) == res
