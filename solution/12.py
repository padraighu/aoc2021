import itertools
from collections import defaultdict
from typing import Dict, List, Set, Tuple

import pytest
from util import read_input

TEST_INPUT, REAL_INPUT = read_input("12")


def parse_input(input: str) -> Dict[str, List[str]]:
    lines = input.splitlines()
    res = defaultdict(list)
    for l in lines:
        a, b = l.split("-")
        res[a].append(b)
        res[b].append(a)
    return res


def part_one(graph: Dict[str, List[str]]) -> int:
    return part_one_helper(graph, "start", [])


def part_one_helper(graph: Dict[str, List[str]], curr: str, visited: List[str]) -> int:
    if curr == "end":
        return 1
    visited.append(curr)
    nbrs = graph[curr]
    res = 0
    for nbr in nbrs:
        if nbr not in visited or nbr.isupper():
            res += part_one_helper(graph, nbr, list(visited))
    return res


def part_two(graph: Dict[str, List[str]]) -> int:
    return part_two_helper(graph, "start", [])


def part_two_helper(graph: Dict[str, List[str]], curr: str, visited: List[str]) -> int:
    if curr == "end":
        return 1
    visited.append(curr)
    nbrs = graph[curr]
    res = 0
    for nbr in nbrs:
        if nbr.isupper():
            can_visit = True
        else:
            if nbr not in visited:
                can_visit = True
            elif nbr != "start":
                cnt = defaultdict(int)  # type: Dict[str, int]
                for v in visited:
                    if v.islower():
                        cnt[v] += 1
                can_visit = True
                for c in cnt.values():
                    if c > 1:
                        can_visit = False
                        break
            else:
                can_visit = False
        if can_visit:
            res += part_two_helper(graph, nbr, list(visited))
    return res


@pytest.mark.parametrize("input, res", [(TEST_INPUT, 226), (REAL_INPUT, 3369)])
def test_part_one(input: str, res: int) -> None:
    assert part_one(parse_input(input)) == res


@pytest.mark.parametrize("input, res", [(TEST_INPUT, 3509), (REAL_INPUT, 85883)])
def test_part_two(input: str, res: int) -> None:
    assert part_two(parse_input(input)) == res
