from typing import List, Set, Tuple

import pytest
from util import read_input

TEST_INPUT, REAL_INPUT = read_input("09")


def parse_input(input: str) -> List[List[int]]:
    return [[int(v) for v in l] for l in input.splitlines()]


def find_low_points(caves: List[List[int]]) -> List[Tuple[int, int]]:
    res = []
    for i in range(len(caves)):
        for j in range(len(caves[i])):
            cave = caves[i][j]
            low_point = True
            if i > 0:
                low_point &= cave < caves[i - 1][j]
            if i < len(caves) - 1:
                low_point &= cave < caves[i + 1][j]
            if j > 0:
                low_point &= cave < caves[i][j - 1]
            if j < len(caves[i]) - 1:
                low_point &= cave < caves[i][j + 1]
            if low_point:
                res.append((i, j))
    return res


def part_one(caves: List[List[int]]) -> int:
    res = 0
    low_points = find_low_points(caves)
    for i, j in low_points:
        res += caves[i][j] + 1
    return res


def find_basin(
    caves: List[List[int]], low_point: Tuple[int, int]
) -> Set[Tuple[int, int]]:
    res = set()
    queue = [low_point]
    while len(queue) > 0:
        i, j = queue.pop()
        if caves[i][j] == 9:
            continue
        res.add((i, j))
        if i > 0 and (i - 1, j) not in res:
            queue.append((i - 1, j))
        if i < len(caves) - 1 and (i + 1, j) not in res:
            queue.append((i + 1, j))
        if j > 0 and (i, j - 1) not in res:
            queue.append((i, j - 1))
        if j < len(caves[i]) - 1 and (i, j + 1) not in res:
            queue.append((i, j + 1))
    return res


def part_two(caves: List[List[int]]) -> int:
    res = 1
    basin_sizes = []
    low_points = find_low_points(caves)
    for low_point in low_points:
        basin = find_basin(caves, low_point)
        basin_sizes.append(len(basin))
    basin_sizes = sorted(basin_sizes, reverse=True)
    for s in basin_sizes[:3]:
        res *= s
    return res


@pytest.mark.parametrize("input, res", [(TEST_INPUT, 15), (REAL_INPUT, 500)])
def test_part_one(input: str, res: int) -> None:
    assert part_one(parse_input(input)) == res


@pytest.mark.parametrize("input, res", [(TEST_INPUT, 1134), (REAL_INPUT, 970200)])
def test_part_two(input: str, res: int) -> None:
    assert part_two(parse_input(input)) == res
