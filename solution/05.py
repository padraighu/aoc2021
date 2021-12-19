from collections import defaultdict
from typing import Dict, List, Tuple

import pytest
from util import read_input

TEST_INPUT, REAL_INPUT = read_input("05")


def parse_input(input: str) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
    lines = input.splitlines()
    lines_parsed = [
        (v[0].split(","), v[1].split(",")) for v in [l.split(" -> ") for l in lines]
    ]
    res = []
    for _idx, l in enumerate(lines_parsed):
        res.append(((int(l[0][0]), int(l[0][1])), (int(l[1][0]), int(l[1][1]))))
    return res


def part_one(lines: List[Tuple[Tuple[int, int], Tuple[int, int]]]) -> int:
    res = 0
    cover = defaultdict(int)  # type: Dict[Tuple[int, int], int]
    for line in lines:
        a, b = line[0], line[1]
        vertical = a[0] == b[0]
        horizontal = a[1] == b[1]
        if horizontal:
            for x in range(min(a[0], b[0]), max(a[0], b[0]) + 1):
                cover[(x, a[1])] += 1
        if vertical:
            for y in range(min(a[1], b[1]), max(a[1], b[1]) + 1):
                cover[(a[0], y)] += 1
    for cnt in cover.values():
        if cnt > 1:
            res += 1
    return res


def part_two(lines: List[Tuple[Tuple[int, int], Tuple[int, int]]]) -> int:
    res = 0
    cover = defaultdict(int)  # type: Dict[Tuple[int, int], int]
    for line in lines:
        a, b = line[0], line[1]
        vertical = a[0] == b[0]
        horizontal = a[1] == b[1]
        delta_x = a[0] - b[0]
        delta_y = a[1] - b[1]
        diagonal = abs(delta_x) == abs(delta_y)
        if horizontal:
            for x in range(min(a[0], b[0]), max(a[0], b[0]) + 1):
                cover[(x, a[1])] += 1
        if vertical:
            for y in range(min(a[1], b[1]), max(a[1], b[1]) + 1):
                cover[(a[0], y)] += 1
        if diagonal:
            if delta_x * delta_y > 0:
                for x, y in zip(
                    range(min(a[0], b[0]), max(a[0], b[0]) + 1),
                    range(min(a[1], b[1]), max(a[1], b[1]) + 1),
                ):
                    cover[(x, y)] += 1
            else:
                for x, y in zip(
                    range(min(a[0], b[0]), max(a[0], b[0]) + 1),
                    range(max(a[1], b[1]), min(a[1], b[1]) - 1, -1),
                ):
                    cover[(x, y)] += 1
    for cnt in cover.values():
        if cnt > 1:
            res += 1
    return res


@pytest.mark.parametrize("input, res", [(TEST_INPUT, 5), (REAL_INPUT, 6189)])
def test_part_one(input: str, res: int) -> None:
    assert part_one(parse_input(input)) == res


@pytest.mark.parametrize("input, res", [(TEST_INPUT, 12), (REAL_INPUT, 19164)])
def test_part_two(input: str, res: int) -> None:
    assert part_two(parse_input(input)) == res
