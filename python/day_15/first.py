"""
--- Day 15: Chiton ---

You've almost reached the exit of the cave, but the walls are getting closer together. 
Your submarine can barely still fit, though; the main problem is that the walls of the cave are covered in chitons, 
and it would be best not to bump any of them.

The cavern is large, but has a very low ceiling, restricting your motion to two dimensions. 
The shape of the cavern resembles a square; a quick scan of chiton density produces a map of risk level throughout the cave (your puzzle input). 
For example:

1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581

You start in the top left position, your destination is the bottom right position, and you cannot move diagonally. 
The number at each position is its risk level; to determine the total risk of an entire path, add up the risk levels of each position 
you enter (that is, don't count the risk level of your starting position unless you enter it; leaving it adds no risk to your total).

Your goal is to find a path with the lowest total risk. In this example, a path with the lowest total risk is highlighted here:

1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581

The total risk of this path is 40 (the starting position is never entered, so its risk is not counted).

What is the lowest total risk of any path from the top left to the bottom right?
"""
import numpy as np
from skimage.graph import route_through_array


def get_shortest_path_cost(costs_map: np.ndarray) -> int:
    """Finds the shortest path in the array and return the calculated cost."""
    path, path_cost = route_through_array(costs_map, start=(0, 0), end=(-1, -1), fully_connected=False, geometric=False)
    return path_cost - costs_map[0, 0]  # we do not count the starting position for the cost


if __name__ == "__main__":
    costs_map = np.genfromtxt("inputs.txt", delimiter=1, dtype=int)
    path_cost = get_shortest_path_cost(costs_map)
    print(path_cost)
