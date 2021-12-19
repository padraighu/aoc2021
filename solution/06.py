from collections import defaultdict
from typing import Dict, List

import pytest
from util import read_input

TEST_INPUT, REAL_INPUT = read_input("06")


def parse_input(input: str) -> List[int]:
    return [int(l) for l in input.split(",")]


def part_one(fish: List[int]) -> int:
    return helper(fish, 80)


def helper(fish: List[int], DAYS: int) -> int:
    res = 0
    cnt = defaultdict(int)  # type: Dict[int, int]
    for f in fish:
        cnt[f] += 1
    for _day in range(DAYS):
        next_cnt = defaultdict(int)
        next_cnt[6] = cnt[0]
        next_cnt[8] = cnt[0]
        for f in cnt:
            if f > 0:
                next_cnt[f - 1] += cnt[f]
        cnt = next_cnt
    res = sum(cnt.values())
    return res


def part_two(fish: List[int]) -> int:
    return helper(fish, 256)


@pytest.mark.parametrize("input, res", [(TEST_INPUT, 5934), (REAL_INPUT, 390923)])
def test_part_one(input: str, res: int) -> None:
    assert part_one(parse_input(input)) == res


@pytest.mark.parametrize(
    "input, res", [(TEST_INPUT, 26984457539), (REAL_INPUT, 1749945484935)]
)
def test_part_two(input: str, res: int) -> None:
    assert part_two(parse_input(input)) == res
