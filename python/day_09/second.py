"""
--- Part Two ---

Next, you need to find the largest basins so you know what areas are most important to avoid.

A basin is all locations that eventually flow downward to a single low point. 
Therefore, every low point has a basin, although some basins are very small. 
Locations of height 9 do not count as being in any basin, and all other locations will always be part of exactly one basin.

The size of a basin is the number of locations within the basin, including the low point. 
The example above has four basins.

The top-left basin, size 3:

2199943210
3987894921
9856789892
8767896789
9899965678

The top-right basin, size 9:

2199943210
3987894921
9856789892
8767896789
9899965678

The middle basin, size 14:

2199943210
3987894921
9856789892
8767896789
9899965678

The bottom-right basin, size 9:

2199943210
3987894921
9856789892
8767896789
9899965678

Find the three largest basins and multiply their sizes together. 
In the above example, this is 9 * 14 * 9 = 1134.

What do you get if you multiply together the sizes of the three largest basins?
"""
from typing import Set, Tuple

import numpy as np
from first import find_low_points_indices, find_neighbours_indices  # let's use these again


# This might be ugly but let's do it recursively
def find_basins(x: int, y: int, heights_map: np.ndarray) -> Set[Tuple[int, int]]:
    """
    Given the coordinates of a low point in the height map, find all points in its basin and
    return the set of their coordinates.
    """
    basin_coordinates = {(x, y)}  # the basin will always include the low point, so we start with that
    for a, b in find_neighbours_indices(x, y, heights_map.shape):
        # The neighbour at [a, b] is in the basin if it's higher than point at [x, y] and if it's lower than a 9
        if heights_map[x, y] < heights_map[a, b] < 9:
            # We can add the neighbour coordinate to our basin, but we need to also look for its neightbours
            # so we will recursively find the basins of all neighbours
            basin_coordinates |= find_basins(a, b, heights_map)
    return basin_coordinates


if __name__ == "__main__":
    heights_map = np.genfromtxt("inputs.txt", delimiter=1, dtype=int)  # 2D array of the inputs as integers
    low_points_indices = find_low_points_indices(heights_map)  # first find the low points as in part 1
    all_basins = [find_basins(index[0], index[1], heights_map) for index in low_points_indices]  # get all basins
    all_basins.sort(key=len, reverse=True)  # sort the basins by length (number of elements in the basin) inplace
    print(len(all_basins[0]) * len(all_basins[1]) * len(all_basins[2]))  # multiply the lenghts of the 3 biggest ones
