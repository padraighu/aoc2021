from typing import List, Tuple

import pytest
from util import read_input

TEST_INPUT, REAL_INPUT = read_input("13")

Paper = List[List[bool]]


def parse_input(input: str) -> Tuple[Paper, List[Tuple[str, int]]]:
    lines = input.splitlines()
    idx = lines.index("")
    marks_str = lines[:idx]
    instructions_str = lines[idx + 1 :]
    marks = []
    max_x, max_y = 0, 0
    for l in marks_str:
        l_split = l.split(",")
        x, y = int(l_split[0]), int(l_split[1])
        marks.append((x, y))
        max_x, max_y = max(max_x, x), max(max_y, y)
    paper = [[False for j in range(max_x + 1)] for i in range(max_y + 1)]
    for mark in marks:
        paper[mark[1]][mark[0]] = True
    instructions = []
    for l in instructions_str:
        l = l.replace("fold along", "").strip()
        l_split = l.split("=")
        instructions.append((l_split[0], int(l_split[1])))
    return paper, instructions


def print_paper(paper: Paper) -> None:
    res = "\n"
    for i in range(len(paper)):
        for j in range(len(paper[i])):
            res += "#" if paper[i][j] else "."
        res += "\n"
    print(res)


def fold_along_y(paper: Paper, val: int) -> Paper:
    new_paper = [[False for j in range(len(paper[i]))] for i in range(val)]
    for y in range(len(paper)):
        for x in range(len(paper[y])):
            if y < val:
                new_paper[y][x] |= paper[y][x]
            elif y > val:
                new_paper[len(paper) - 1 - y][x] |= paper[y][x]
    return new_paper


def fold_along_x(paper: Paper, val: int) -> Paper:
    new_paper = [[False for j in range(val)] for i in range(len(paper))]
    for y in range(len(paper)):
        for x in range(len(paper[y])):
            if x < val:
                new_paper[y][x] |= paper[y][x]
            elif x > val:
                new_paper[y][len(paper[y]) - 1 - x] |= paper[y][x]
    return new_paper


def count_visible(paper: Paper) -> int:
    res = 0
    for y in range(len(paper)):
        for x in range(len(paper[y])):
            if paper[y][x]:
                res += 1
    return res


def part_one(paper: Paper, instructions: List[Tuple[str, int]]) -> int:
    res = 0
    for axis, val in instructions[:1]:
        if axis == "y":
            paper = fold_along_y(paper, val)
        if axis == "x":
            paper = fold_along_x(paper, val)
    res = count_visible(paper)
    return res


def part_two(paper: Paper, instructions: List[Tuple[str, int]]) -> Paper:
    for axis, val in instructions:
        if axis == "y":
            paper = fold_along_y(paper, val)
        if axis == "x":
            paper = fold_along_x(paper, val)
    return paper


@pytest.mark.parametrize("input, res", [(TEST_INPUT, 17), (REAL_INPUT, 802)])
def test_part_one(input: str, res: int) -> None:
    paper, instructions = parse_input(input)
    assert part_one(paper, instructions) == res


if __name__ == "__main__":
    paper, instructions = parse_input(REAL_INPUT)
    print_paper(part_two(paper, instructions))
