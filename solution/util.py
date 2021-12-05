from typing import Tuple

def read_input(day: str) -> Tuple[str]:
    with open(f'../input/{day}t.txt', 'r') as f:
        test_input = f.read()

    with open(f'../input/{day}r.txt', 'r') as f:
        real_input = f.read()
    return test_input, real_input