#!/bin/python3

"""
Author: Jakub Lisowski, 2024
MIT License
"""
import random
import time
import argparse

def prepare_cpp_array_init_lis(strs: list[str]) -> str:
    return "{\n" + ", ".join([f"\t{s}," for s in strs]) + "};\n"


def prepare_cpp_array_init(strs: list[str], array_name: str, typename: str) -> str:
    return f"{typename} {array_name}[] = {prepare_cpp_array_init_lis(strs)}"


def generate_random_seed(count: int) -> list[int]:
    random.seed(time.time())

    return [random.randint(0, 2 ** 32 - 1) for _ in range(count)]


# for each modulo value, generate 'count' random seeds
def generate_pseudo_random_seed_modulo(count: int, modulo: int) -> list[int]:
    if count == 0:
        return []

    random.seed(time.time())

    rv = []
    for expected_mod in range(modulo):
        counter = count

        while counter > 0:
            seed = random.randint(0, 2 ** 32 - 1)
            if seed % modulo == expected_mod:
                rv.append(seed)
                counter -= 1

    return rv


def random_seed_gen(count_random_seeds: int, count_modulo_seeds: int, modulo: int) -> None:
    random_seeds = generate_random_seed(count_random_seeds)
    modulo_seeds = generate_pseudo_random_seed_modulo(count_modulo_seeds, modulo)

    print("Random seeds:")
    print(prepare_cpp_array_init_lis([str(seed) for seed in random_seeds]))
    print("Modulo seeds:")
    print(prepare_cpp_array_init_lis([str(seed) for seed in modulo_seeds]))


def main():
    parser = argparse.ArgumentParser(description="Generate random seeds and modulo random seeds.")
    parser.add_argument(
        "--count_random",
        type=int,
        default=0,
        help="Number of random seeds to generate."
    )
    parser.add_argument(
        "--count_modulo",
        type=int,
        default=0,
        help="Number of modulo-specific seeds to generate for each modulo value."
    )
    parser.add_argument(
        "--modulo",
        type=int,
        default=1,
        help="Modulo value for generating modulo-specific seeds. Must be greater than 0."
    )

    args = parser.parse_args()

    if args.modulo <= 0:
        print("Error: The modulo value must be greater than 0.")
        return

    random_seed_gen(args.count_random, args.count_modulo, args.modulo)


if __name__ == "__main__":
    main()
