from collections import deque
from typing import Deque, List

import pytest
from util import read_input

TEST_INPUT, REAL_INPUT = read_input("10")


def parse_input(input: str) -> List[str]:
    return [l for l in input.splitlines() if len(l) > 0]


def part_one(lines: List[str]) -> int:
    res = 0
    match = {"(": ")", "[": "]", "{": "}", "<": ">"}
    score = {")": 3, "]": 57, "}": 1197, ">": 25137}
    for l in lines:
        stack = deque()  # type: Deque[str]
        illegal = None
        for c in l:
            if c in match.keys():
                stack.append(c)
            else:
                curr = stack.pop()
                if c != match[curr]:
                    illegal = c
                    break
        if illegal:
            res += score[illegal]
    return res


def part_two(lines: List[str]) -> int:
    res = 0
    match = {"(": ")", "[": "]", "{": "}", "<": ">"}
    score = {")": 1, "]": 2, "}": 3, ">": 4}
    line_scores = []
    for l in lines:
        line_score = 0
        stack = deque()  # type: Deque[str]
        illegal = None
        for c in l:
            if c in match.keys():
                stack.append(c)
            else:
                curr = stack.pop()
                if c != match[curr]:
                    illegal = c
                    break
        if not illegal:
            autocomplete = "".join([match[c] for c in reversed(stack)])
            for c in autocomplete:
                line_score = 5 * line_score + score[c]
            line_scores.append(line_score)
    line_scores = sorted(line_scores)
    res = line_scores[int(len(line_scores) / 2)]
    return res


@pytest.mark.parametrize("input, res", [(TEST_INPUT, 26397), (REAL_INPUT, 362271)])
def test_part_one(input: str, res: int) -> None:
    assert part_one(parse_input(input)) == res


@pytest.mark.parametrize("input, res", [(TEST_INPUT, 288957), (REAL_INPUT, 1698395182)])
def test_part_two(input: str, res: int) -> None:
    assert part_two(parse_input(input)) == res
