from typing import List, Tuple

import pytest
from util import read_input

TEST_INPUT, REAL_INPUT = read_input("04")


def parse_input(input: str) -> Tuple[List[int], List[List[List[int]]]]:
    lines = input.splitlines()
    draw = [int(n) for n in lines[0].split(",")]
    lines_parsed = [
        [int(n.strip()) for n in l.split(" ") if len(n.strip()) > 0]
        for l in lines[2:]
        if len(l) > 0
    ]
    boards = []
    for i in range(int(len(lines_parsed) / 5)):
        board = []
        for j in range(5):
            board.append(lines_parsed[i * 5 + j])
        boards.append(board)
    # print(boards)
    return draw, boards


def part_one(draw: List[int], boards: List[List[List[int]]]) -> int:
    res = 0
    winner = False
    for i in range(len(draw) - 5):
        curr = draw[: i + 5]
        for board in boards:
            winner = check_winner(curr, board)
            if winner:
                the_sum = sum_of_unmarked(curr, board)
                the_num = curr[-1]
                res = the_sum * the_num
                return res
    return -1


def check_winner(draw: List[int], board: List[List[int]]) -> bool:
    # check rows, then columns
    to_check = set(draw)
    for row in board:
        winner = set(row).issubset(to_check)
        if winner:
            return winner
    ncol = len(board[0])
    cols = [[row[col] for row in board] for col in range(ncol)]
    for col in cols:
        winner = set(col).issubset(to_check)
        if winner:
            return winner
    return False


def sum_of_unmarked(marked: List[int], board: List[List[int]]) -> int:
    res = 0
    for row in board:
        for val in row:
            if val not in marked:
                res += val
    return res


def part_two(draw: List[int], boards: List[List[List[int]]]) -> int:
    res = 0
    winner = False
    already_won = []
    for i in range(len(draw) - 5):
        curr = draw[: i + 5]
        for board in boards:
            if board not in already_won:
                winner = check_winner(curr, board)
                if winner:
                    already_won.append(board)
                    last_winning_draw = curr
                    last_winning_board = board
    assert winner
    the_sum = sum_of_unmarked(last_winning_draw, last_winning_board)
    the_num = last_winning_draw[-1]
    res = the_sum * the_num
    return res


@pytest.mark.parametrize("input, res", [(TEST_INPUT, 4512), (REAL_INPUT, 12796)])
def test_part_one(input: str, res: int) -> None:
    draw, boards = parse_input(input)
    assert part_one(draw, boards) == res


@pytest.mark.parametrize("input, res", [(TEST_INPUT, 1924), (REAL_INPUT, 18063)])
def test_part_two(input: str, res: int) -> None:
    draw, boards = parse_input(input)
    assert part_two(draw, boards) == res
