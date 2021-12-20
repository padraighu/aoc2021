from collections import Counter
from typing import Dict, Tuple

import pytest
from util import read_input

TEST_INPUT, REAL_INPUT = read_input("14")


def parse_input(input: str) -> Tuple[str, Dict[str, str]]:
    lines = input.splitlines()
    idx = lines.index("")
    template = lines[0]
    rules_str = lines[idx + 1 :]
    rules = {}
    for r in rules_str:
        r_split = r.split("->")
        adj = r_split[0].strip()
        insert = r_split[1].strip()
        rules[adj] = insert
    return template, rules


def helper(template: str, rules: Dict[str, str], steps: int) -> int:
    res = 0
    pairs = ["".join(p) for p in zip(template, template[1:])]
    cnt = Counter(pairs)
    element_cnt = Counter(template)
    for _step in range(steps):
        next_cnt = Counter()  # type: Counter[str]
        for pair in cnt:
            if pair in rules:
                insert = rules[pair]
                pair_a, pair_b = pair[0] + insert, insert + pair[1]
                next_cnt[pair_a] += cnt[pair]
                next_cnt[pair_b] += cnt[pair]
                element_cnt[insert] += cnt[pair]
        cnt = next_cnt
    tally = element_cnt.values()
    most_common, least_common = max(tally), min(tally)
    res = most_common - least_common
    return res


def part_one(template: str, rules: Dict[str, str]) -> int:
    res = helper(template, rules, 10)
    return res


def part_two(template: str, rules: Dict[str, str]) -> int:
    res = helper(template, rules, 40)
    return res


@pytest.mark.parametrize("input, res", [(TEST_INPUT, 1588), (REAL_INPUT, 2797)])
def test_part_one(input: str, res: int) -> None:
    template, rules = parse_input(input)
    assert part_one(template, rules) == res


@pytest.mark.parametrize(
    "input, res", [(TEST_INPUT, 2188189693529), (REAL_INPUT, 2926813379532)]
)
def test_part_two(input: str, res: int) -> None:
    template, rules = parse_input(input)
    assert part_two(template, rules) == res
