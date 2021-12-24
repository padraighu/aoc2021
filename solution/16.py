import math
from typing import List, Tuple

import pytest
from util import read_input

TEST_INPUT, REAL_INPUT = read_input("16")

hex_to_bin_mapping = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111",
}


def parse_input(input: str) -> str:
    return input.strip()


def hex_to_bin(packet: str) -> str:
    packet_bin = packet
    for h, b in hex_to_bin_mapping.items():
        packet_bin = packet_bin.replace(h, b)
    return packet_bin


def decode_literal_value(packet_bin: str) -> Tuple[str, int]:
    val_packet = packet_bin[6:]
    val_str = ""
    idx = 0
    while True:
        five_bits = val_packet[idx : idx + 5]
        val_str += five_bits[1:]
        idx += 5
        if five_bits[0] == "0":
            break
    remaining_packets = val_packet[idx:]
    literal_value = int(val_str, 2)
    return remaining_packets, literal_value


def decode_operator(packet_bin: str, versions: List[int]) -> Tuple[str, List[int]]:
    op_packet = packet_bin[6:]
    length_type_id = op_packet[0]
    vals = []
    if length_type_id == "0":
        total_length_bits = int(op_packet[1:16], 2)
        remaining_packets = op_packet[16:]
        prev_len = len(remaining_packets)
        while prev_len - len(remaining_packets) < total_length_bits:
            remaining_packets, val = decode_packet(remaining_packets, versions)
            vals += [val]
    else:
        num_of_sub_packets = int(op_packet[1:12], 2)
        packets_consumed = 0
        remaining_packets = op_packet[12:]
        while packets_consumed < num_of_sub_packets:
            remaining_packets, val = decode_packet(remaining_packets, versions)
            vals += [val]
            packets_consumed += 1
    return remaining_packets, vals


def decode_packet(packet_bin: str, versions: List[int]) -> Tuple[str, int]:
    version = int(packet_bin[:3], 2)
    versions += [version]
    type_id = int(packet_bin[3:6], 2)
    if type_id == 4:
        # literal value
        remaining_packets, val = decode_literal_value(packet_bin)
    else:
        # operator
        remaining_packets, vals = decode_operator(packet_bin, versions)
        if type_id == 0:
            val = sum(vals)
        if type_id == 1:
            val = math.prod(vals)
        if type_id == 2:
            val = min(vals)
        if type_id == 3:
            val = max(vals)
        if type_id == 5:
            assert len(vals) == 2
            val = 1 if vals[0] > vals[1] else 0
        if type_id == 6:
            assert len(vals) == 2
            val = 1 if vals[0] < vals[1] else 0
        if type_id == 7:
            assert len(vals) == 2
            val = 1 if vals[0] == vals[1] else 0
    return remaining_packets, val


def part_one(packet: str) -> int:
    res = 0
    packet_bin = hex_to_bin(packet)
    versions = []  # type: List[int]
    _remaining_packets, _val = decode_packet(packet_bin, versions)
    version_sum = sum(versions)
    res = version_sum
    return res


def part_two(packet: str) -> int:
    res = 0
    packet_bin = hex_to_bin(packet)
    versions = []  # type: List[int]
    _remaining_packets, val = decode_packet(packet_bin, versions)
    res = val
    return res


@pytest.mark.parametrize(
    "input, res",
    [
        ("D2FE28", 6),
        ("38006F45291200", 9),
        ("EE00D40C823060", 14),
        ("8A004A801A8002F478", 16),
        ("620080001611562C8802118E34", 12),
        ("C0015000016115A2E0802F182340", 23),
        ("A0016C880162017C3686B18A3D4780", 31),
        (REAL_INPUT, 852),
    ],
)
def test_part_one(input: str, res: int) -> None:
    all_flag = True
    if all_flag or input == "620080001611562C8802118E34":
        assert part_one(parse_input(input)) == res


@pytest.mark.parametrize(
    "input, res",
    [
        ("C200B40A82", 3),
        ("04005AC33890", 54),
        ("880086C3E88112", 7),
        ("CE00C43D881120", 9),
        ("D8005AC2A8F0", 1),
        ("F600BC2D8F", 0),
        ("9C005AC2F8F0", 0),
        ("9C0141080250320F1802104A08", 1),
        (REAL_INPUT, 19348959966392),
    ],
)
def test_part_two(input: str, res: int) -> None:
    assert part_two(parse_input(input)) == res
