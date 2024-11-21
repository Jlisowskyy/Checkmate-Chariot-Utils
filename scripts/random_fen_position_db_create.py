"""
Author: Jakub Lisowski, 2024
MIT License
"""

import argparse
import random
import sys
import time
from itertools import cycle
from threading import Thread, Event

import chess.pgn as chs
from tqdm import tqdm


class LoadingAnimation:
    def __init__(self, desc: str = "Loading") -> None:
        self.desc = desc
        self.done = Event()
        self.animation = Thread(target=self._animate)

    def _animate(self) -> None:
        for dots in cycle([".  ", ".. ", "..."]):
            if self.done.is_set():
                break
            sys.stdout.write(f'\r{self.desc}{dots}')
            sys.stdout.flush()
            time.sleep(0.3)

    def __enter__(self) -> "LoadingAnimation":
        self.animation.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.done.set()
        self.animation.join()
        sys.stdout.write('\r' + ' ' * (len(self.desc) + 4) + '\r')
        sys.stdout.flush()


def load_games(pgn_file: str) -> list[chs.Game]:
    games = []

    with LoadingAnimation("Loading games"):
        with open(pgn_file, "r", encoding='latin-1') as file:
            while True:
                game = chs.read_game(file)
                if game is None:
                    break
                games.append(game)

    print(f"Loaded {len(games)} games")
    return games


def pick_random_position(games_with_min_moves: list[chs.Game], min_moves: int,
                         max_moves: int) -> str:
    num = random.randint(0, len(games_with_min_moves) - 1)
    game = games_with_min_moves[num]

    move_count = len([move for move in game.mainline_moves()])
    move_num = random.randint(min_moves, min(move_count, max_moves))

    board = game.board()
    counter = 0
    for move in game.mainline_moves():
        board.push(move)
        counter += 1

        if counter == move_num:
            return board.fen()


def generate_db(pgn_file: str, out_path: str, min_moves: int, max_moves: int,
                output_size: int) -> None:
    games = load_games(pgn_file)
    games_with_min_moves = []

    with tqdm(total=len(games), desc="Filtering games") as pbar:
        for game in games:
            if len([move for move in game.mainline_moves()]) >= min_moves:
                games_with_min_moves.append(game)

            pbar.update(1)

    if len(games_with_min_moves) == 0:
        raise ValueError("No games with min_moves")

    db = []
    with tqdm(total=output_size, desc="Generating positions") as pbar:
        for i in range(output_size):
            db.append(pick_random_position(games_with_min_moves, min_moves, max_moves))
            pbar.update(1)

    print(f"Writing database to {out_path}")
    with open(out_path, "w") as file:
        for position in db:
            file.write(position + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Generate a database of chess positions from PGN files')

    parser.add_argument('--pgn-file', type=str, required=True,
                        help='Path to input PGN file')
    parser.add_argument('--out-path', type=str, required=True,
                        help='Path to output file')
    parser.add_argument('--min-moves', type=int, default=10,
                        help='Minimum number of moves to consider (default: 10)')
    parser.add_argument('--max-moves', type=int, default=40,
                        help='Maximum number of moves to consider (default: 40)')
    parser.add_argument('--output-size', type=int, default=1000,
                        help='Number of positions to generate (default: 1000)')

    args = parser.parse_args()

    try:
        generate_db(args.pgn_file, args.out_path, args.min_moves, args.max_moves, args.output_size)
        print(f"Successfully generated database at {args.out_path}")
    except Exception as e:
        print(f"Failed with error: {e}")


if __name__ == "__main__":
    main()
