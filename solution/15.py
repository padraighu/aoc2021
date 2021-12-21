import heapq
from typing import Dict, List, Set, Tuple

import pytest
from util import read_input

TEST_INPUT, REAL_INPUT = read_input("15")

Node = Tuple[int, int]
WeightedGraph = Dict[Node, List[Tuple[Node, int]]]


def parse_input(input: str, part_one: bool = True) -> Tuple[WeightedGraph, Node, Node]:
    matrix = [[int(c) for c in r] for r in input.splitlines()]
    graph = dict()  # type: WeightedGraph
    deltas = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    nrow = len(matrix)
    ncol = len(matrix[0])
    if not part_one:
        full_matrix = [
            [matrix[i % nrow][j % ncol] for j in range(5 * ncol)]
            for i in range(5 * nrow)
        ]
        for i in range(nrow):
            for j in range(ncol):
                for delta_i in range(5):
                    for delta_j in range(5):
                        x = i + delta_i * nrow
                        y = j + delta_j * ncol
                        full_matrix[x][y] += delta_i + delta_j
                        while full_matrix[x][y] > 9:
                            full_matrix[x][y] -= 9
        matrix = full_matrix
    nrow = len(matrix)
    ncol = len(matrix[0])
    for i in range(nrow):
        for j in range(ncol):
            nbrs = [
                ((i + x, j + y), matrix[i + x][j + y])
                for x, y in deltas
                if 0 <= i + x < nrow and 0 <= j + y < ncol
            ]
            graph[(i, j)] = nbrs
    return graph, (0, 0), (nrow - 1, ncol - 1)


def find_shortest_path(graph: WeightedGraph, start: Node, end: Node) -> int:
    # Dijkstra
    visited = set()  # type: Set[Node]
    dist = {n: float("inf") for n in graph}
    dist[start] = 0
    queue = [(dist[start], start)]
    while len(queue) > 0:
        curr_dist, curr = heapq.heappop(queue)
        if curr == end:
            break
        visited.add(curr)
        for nbr, cost in graph[curr]:
            if nbr not in visited:
                curr_cost = curr_dist + cost
                if curr_cost < dist[nbr]:
                    dist[nbr] = curr_cost
                    heapq.heappush(queue, (curr_cost, nbr))
    return int(dist[end])


def part_one(graph: WeightedGraph, start: Node, end: Node) -> int:
    res = find_shortest_path(graph, start, end)
    return res


def part_two(graph: WeightedGraph, start: Node, end: Node) -> int:
    res = find_shortest_path(graph, start, end)
    return res


@pytest.mark.parametrize("input, res", [(TEST_INPUT, 40), (REAL_INPUT, 540)])
def test_part_one(input: str, res: int) -> None:
    graph, start, end = parse_input(input, part_one=True)
    assert part_one(graph, start, end) == res


@pytest.mark.parametrize("input, res", [(TEST_INPUT, 315), (REAL_INPUT, 2879)])
def test_part_two(input: str, res: int) -> None:
    graph, start, end = parse_input(input, part_one=False)
    assert part_two(graph, start, end) == res
