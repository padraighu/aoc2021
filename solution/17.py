import math
import re
from dataclasses import dataclass
from typing import Tuple

import pytest
from util import read_input

TEST_INPUT, REAL_INPUT = read_input("17")

Range = Tuple[int, int]
Coord = Tuple[int, int]
Velocity = Tuple[int, int]


@dataclass
class Area:
    x_interval: Range
    y_interval: Range


def parse_input(input: str) -> Area:
    input_pattern = (
        r"target area: x=([0-9\-]+)\.\.([0-9\-]+), y=([0-9\-]+)\.\.([0-9\-]+)"
    )
    match = re.match(input_pattern, input.strip())
    if match:
        res = Area(
            x_interval=(int(match[1]), int(match[2])),
            y_interval=(int(match[3]), int(match[4])),
        )
    else:
        raise ValueError("Failed to parse input")
    return res


def probe_position(coord: Coord, velocity: Velocity) -> Tuple[Coord, Velocity]:
    new_coord = (coord[0] + velocity[0], coord[1] + velocity[1])
    delta_x = 1 if velocity[0] < 0 else -1 if velocity[0] > 0 else 0
    new_velocity = (velocity[0] + delta_x, velocity[1] - 1)
    return new_coord, new_velocity


def in_target_area(coord: Coord, target: Area) -> bool:
    res = (
        target.x_interval[0] <= coord[0] <= target.x_interval[1]
        and target.y_interval[0] <= coord[1] <= target.y_interval[1]
    )
    return res


def check_velocity(velocity: Velocity, target: Area) -> Tuple[bool, int]:
    coord = (0, 0)
    step = 0
    max_y = -math.inf
    while True:
        step += 1
        coord, velocity = probe_position(coord, velocity)
        max_y = max(max_y, coord[1])
        if in_target_area(coord, target):
            return True, int(max_y)
        if coord[1] <= target.y_interval[0] or coord[0] > target.x_interval[1]:
            return False, int(max_y)


def part_one(target: Area) -> int:
    res = 0
    max_max_y = -math.inf
    for y in range(100, -101, -1):
        for x in range(-50, 51):
            v = (x, y)
            hits_target, max_y = check_velocity(v, target)
            if hits_target:
                max_max_y = max(max_max_y, max_y)
    res = int(max_max_y)
    return res


def part_two(target: Area) -> int:
    res = 0
    max_max_y = -math.inf
    for y in range(target.y_interval[0], abs(target.y_interval[0])):
        for x in range(0, target.x_interval[1] + 1):
            v = (x, y)
            hits_target, max_y = check_velocity(v, target)
            if hits_target:
                max_max_y = max(max_max_y, max_y)
                res += 1
    return res


@pytest.mark.parametrize("input, res", [(TEST_INPUT, 45), (REAL_INPUT, 5050)])
def test_part_one(input: str, res: int) -> None:
    assert part_one(parse_input(input)) == res


@pytest.mark.parametrize("input, res", [(TEST_INPUT, 112), (REAL_INPUT, 2223)])
def test_part_two(input: str, res: int) -> None:
    assert part_two(parse_input(input)) == res
