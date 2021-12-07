"""
--- Part Two ---

Suppose the lanternfish live forever and have unlimited food and space.
Would they take over the entire ocean?

After 256 days in the example above, there would be a total of 26984457539 lanternfish!

How many lanternfish would there be after 256 days?
"""
# This is exactly part 1 with a different value call
import numpy as np


def reproduce(initial_fishes: np.ndarray, days: int) -> np.ndarray:
    """Reproduce the fishes through the days, return the final distribution"""
    unique, counts = np.unique(initial_fishes, return_counts=True)  # find how many fishes are for each countdown value

    # This array will keep count of the number of fishes with each countdown value
    fishes = np.zeros(9, dtype=int)
    fishes[unique] = counts  # we initialize it with the input

    for index in range(days):
        fishes_at_zero = fishes[0]
        fishes[:-1] = fishes[1:]  # shift the array by 1 as all fishes countdown values decrease
        fishes[8] = fishes_at_zero  # those that were at 0 spawn new fishes which start at 8
        fishes[6] += fishes_at_zero  # those that were at 0 reset at 6 after spawning a new fish
    return np.sum(fishes)


if __name__ == "__main__":
    initial_lanternfishes = np.loadtxt("inputs.txt", delimiter=",", dtype=int)
    print(reproduce(initial_lanternfishes, 256))
