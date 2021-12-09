"""
--- Day 9: Smoke Basin ---

These caves seem to be lava tubes.
Parts are even still volcanically active; small hydrothermal vents release smoke into the caves that slowly settles like rain.

If you can model how the smoke flows through the caves, you might be able to avoid it and be that much safer.
The submarine generates a heightmap of the floor of the nearby caves for you (your puzzle input).

Smoke flows to the lowest point of the area it's in. 
For example, consider the following heightmap:

2199943210
3987894921
9856789892
8767896789
9899965678

Each number corresponds to the height of a particular location, where 9 is the highest and 0 is the lowest a location can be.

Your first goal is to find the low points - the locations that are lower than any of its adjacent locations. 
Most locations have four adjacent locations (up, down, left, and right); locations on the edge or corner of the map have three or 
two adjacent locations, respectively. (Diagonal locations do not count as adjacent.)

In the above example, there are four low points, all highlighted: two are in the first row (a 1 and a 0), one is in the third row (a 5), 
and one is in the bottom row (also a 5). All other locations on the heightmap have some lower adjacent location, and so are not low points.

The risk level of a low point is 1 plus its height. In the above example, the risk levels of the low points are 2, 1, 6, and 6. 
The sum of the risk levels of all low points in the heightmap is therefore 15.

Find all of the low points on your heightmap. 
What is the sum of the risk levels of all low points on your heightmap?
"""
from typing import List, Tuple

import numpy as np


def find_neighbours_indices(x: int, y: int, inputs_shape: Tuple[int, int]) -> List[Tuple[int, int]]:
    """
    Given the indices for a point at position [x, y] in the array,
    returns the indices of its valid neighbours (no diagonal neighbours).
    """
    neighbour_indices = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    return [(a, b) for a, b in neighbour_indices if 0 <= a < inputs_shape[0] and 0 <= b < inputs_shape[1]]


def find_low_points_indices(heightmap: np.ndarray) -> np.ndarray:
    """Determine low points and return the list of their locations' indices."""
    low_points_indices = []

    # Just iterate through the whole array, and check against the neighbours at each position
    for x in range(heightmap.shape[0]):
        for y in range(heightmap.shape[1]):
            neighbours = find_neighbours_indices(x, y, heightmap.shape)
            # should be smaller than all neighbours to be a low point
            if all(heightmap[x, y] < heightmap[a][b] for a, b in neighbours):
                low_points_indices.append((x, y))
    return low_points_indices


if __name__ == "__main__":
    heights_map = np.genfromtxt("inputs.txt", delimiter=1, dtype=int)  # 2D array of the inputs as integers
    low_points_indices = find_low_points_indices(heights_map)
    print(sum(heights_map[a][b] + 1 for a, b in low_points_indices))
