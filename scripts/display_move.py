#!/bin/python3

"""
Author: Jakub Lisowski, 2024
MIT License
"""

import sys

BIT6_MASK = 0b111111
FROM_MASK = BIT6_MASK
TO_MASK = BIT6_MASK << 6
PROMO_FLAG = 0b1000
PROMO_MASK = PROMO_FLAG << 12


def get_long_algebraic(move: int) -> str:
    from_square = move & FROM_MASK
    to_square = (move & TO_MASK) >> 6

    from_file = from_square & 7
    from_rank = from_square >> 3
    to_file = to_square & 7
    to_rank = to_square >> 3

    if move & PROMO_FLAG:
        raise NotImplementedError("Promotion not implemented")

    return f"{chr(from_file + 97)}{from_rank + 1}{chr(to_file + 97)}{to_rank + 1}"


def main(args: list[str]) -> None:
    if len(args) != 1:
        print("Usage: display_move.py <move integer>")
        return

    move = int(args[0])
    print(get_long_algebraic(move))


if __name__ == "__main__":
    main(sys.argv[1:])
