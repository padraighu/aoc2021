import pytest
from typing import List, Tuple
from util import read_input

TEST_INPUT, REAL_INPUT = read_input('02')

def parse_input(input: str) -> List[Tuple[str, int]]:
    res = []
    lines = input.splitlines()
    for l in lines:
        splited = l.split(' ')
        res.append((splited[0], int(splited[1])))
    return res

def part_one(input: List[Tuple[str, int]]) -> int:
    res = 0
    x, depth = 0, 0
    for cmd, val in input:
        if cmd == 'forward':
            x += val
        if cmd == 'down':
            depth += val
        if cmd == 'up':
            depth -= val
    res = x * depth
    return res

def part_two(input: List[Tuple[str, int]]) -> int:
    res = 0
    x, depth, aim = 0, 0, 0
    for cmd, val in input:
        if cmd == 'forward':
            x += val
            depth += aim * val
        if cmd == 'down':
            aim += val
        if cmd == 'up':
            aim -= val
    res = x * depth
    return res

@pytest.mark.parametrize('input, res', [(TEST_INPUT, 150), (REAL_INPUT, 2091984)])
def test_part_one(input: str, res: int) -> None:
    assert part_one(parse_input(input)) == res

@pytest.mark.parametrize('input, res', [(TEST_INPUT, 900), (REAL_INPUT, 2086261056)])
def test_part_two(input: str, res: int) -> None:
    assert part_two(parse_input(input)) == res