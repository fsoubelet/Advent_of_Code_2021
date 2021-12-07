"""--- Part Two ---

The crabs don't seem interested in your proposed solution.
Perhaps you misunderstand crab engineering?

As it turns out, crab submarine engines don't burn fuel at a constant rate. 
Instead, each change of 1 step in horizontal position costs 1 more unit of fuel than the last: the first step costs 1, the second step costs 2, the third step costs 3, and so on.

As each crab moves, moving further becomes more expensive. 
This changes the best horizontal position to align them all on; in the example above, this becomes 5:

    Move from 16 to 5: 66 fuel
    Move from 1 to 5: 10 fuel
    Move from 2 to 5: 6 fuel
    Move from 0 to 5: 15 fuel
    Move from 4 to 5: 1 fuel
    Move from 2 to 5: 6 fuel
    Move from 7 to 5: 3 fuel
    Move from 1 to 5: 10 fuel
    Move from 2 to 5: 6 fuel
    Move from 14 to 5: 45 fuel

This costs a total of 168 fuel. 
This is the new cheapest possible outcome; the old alignment position (2) now costs 206 fuel instead.

Determine the horizontal position that the crabs can align to using the least fuel possible so they can make you an escape route! 
How much fuel must they spend to align to that position?
"""
# This is essentially part 1 but with a different way to calculate the fuel cost
# Note: crabs have very bad engineering in these submarines!

import numpy as np


def fuel_cost_from_distance(n: int) -> int:
    """Calculates the fuel cost to move n steps, which is the addition of n + n-1 + ... + 1."""
    return n * (n + 1) // 2


fuel_cost_from_distance = np.vectorize(fuel_cost_from_distance)


def get_distances_arrays(original_positions: np.ndarray) -> np.ndarray:
    """
    Given the original horizontal positions, calculates for each submarine the distance to each position.
    The distance is the absolute value of the difference between the two elements.
    The returned array is a matrix of size (original_positions.size, original_positions.size), and each
    entry is an array with the distances to a given horizontal position.

    The first entry hold the distance of each element to the horizontal position 0.
    The second entry holds the distance of each element to the horizontal position 1.
    Etc...
    """
    distance_array = np.array([[x] * original_positions.shape[0] for x in np.arange(0, np.max(original_positions))])
    return np.abs(distance_array - original_positions)


if __name__ == "__main__":
    original_positions = np.loadtxt("inputs.txt", delimiter=",", dtype=int)
    distances_array = get_distances_arrays(original_positions)
    fuel_costs = fuel_cost_from_distance(distances_array).sum(
        axis=1
    )  # sum all moves necessary to get to each position to get the fuel costs for each
    print(min(fuel_costs))  # minimum fuel cost of all possible combinations
