from typing import List, Tuple

import pytest
from util import read_input

TEST_INPUT, REAL_INPUT = read_input("08")


def parse_input(input: str) -> Tuple[List[List[str]], List[List[str]]]:
    lines = input.splitlines()
    patterns = []
    output = []
    for line in lines:
        splited = line.split("|")
        patterns.append(splited[0].strip().split())
        output.append(splited[1].strip().split())
    return patterns, output


def part_one(output: List[List[str]]) -> int:
    res = 0
    unique_cnts = (2, 4, 3, 7)
    for o in output:
        digit_cnts = [len(set(p)) for p in o]
        res += len([c for c in digit_cnts if c in unique_cnts])
    return res


def part_two(patterns: List[List[str]], output: List[List[str]]) -> int:
    res = 0
    unique_cnts = {2: 1, 4: 4, 3: 7, 7: 8}
    original = {
        "abcefg": 0,
        "cf": 1,
        "acdeg": 2,
        "acdfg": 3,
        "bcdf": 4,
        "abdfg": 5,
        "abdefg": 6,
        "acf": 7,
        "abcdefg": 8,
        "abcdfg": 9,
    }
    for idx in range(len(patterns)):
        encoded = {}  # encoded char to orginal char
        mapping = {}  # digit to encoded pattern
        for p in patterns[idx]:
            cnt = len(set(p))
            if cnt in unique_cnts.keys():
                mapping[unique_cnts[cnt]] = "".join(sorted(p))
                if len(mapping) == 4:
                    break
        a_sus = set(mapping[7]).difference(set(mapping[1]))
        assert len(a_sus) == 1
        bd_sus = set(mapping[4]).difference(set(mapping[1]))
        assert len(bd_sus) == 2
        encoded[a_sus.pop()] = "a"
        zero_six_nine = ["".join(sorted(p)) for p in patterns[idx] if len(p) == 6]
        for sus in zero_six_nine:
            if not set(mapping[1]).issubset(sus):  # 6
                mapping[6] = sus
                for c in mapping[1]:
                    if c not in sus:
                        encoded[c] = "c"
                    else:
                        encoded[c] = "f"
            elif not bd_sus.issubset(sus):  # 0
                mapping[0] = sus
                for c in bd_sus:
                    if c not in sus:
                        encoded[c] = "d"
                    else:
                        encoded[c] = "b"
            else:  # 9
                mapping[9] = sus
                e_sus = set(mapping[8]).difference(set(sus))
                assert len(e_sus) == 1
                encoded[e_sus.pop()] = "e"
        assert len(zero_six_nine) == 3
        g_sus = set(mapping[8]).difference(set(encoded.keys()))
        assert len(g_sus) == 1
        encoded[g_sus.pop()] = "g"
        translated_output = ""
        for o in output[idx]:
            translated = ""
            for c in "".join(sorted(o)):
                translated += encoded[c]
            digit = original["".join(sorted(translated))]
            translated_output += str(digit)
        res += int(translated_output)
    return res


@pytest.mark.parametrize("input, res", [(TEST_INPUT, 26), (REAL_INPUT, 381)])
def test_part_one(input: str, res: int) -> None:
    _patterns, output = parse_input(input)
    assert part_one(output) == res


@pytest.mark.parametrize("input, res", [(TEST_INPUT, 61229), (REAL_INPUT, 1023686)])
def test_part_two(input: str, res: int) -> None:
    patterns, output = parse_input(input)
    assert part_two(patterns, output) == res
