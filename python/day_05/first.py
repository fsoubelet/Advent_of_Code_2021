"""
--- Day 5: Hydrothermal Venture ---

You come across a field of hydrothermal vents on the ocean floor!
These vents constantly produce large, opaque clouds, so it would be best to avoid them if possible.

They tend to form in lines; the submarine helpfully produces a list of nearby lines of vents (your puzzle input) for you to review.
For example:

0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2

Each line of vents is given as a line segment in the format x1,y1 -> x2,y2 where x1,y1 are the coordinates of one end the 
line segment and x2,y2 are the coordinates of the other end.
These line segments include the points at both ends. In other words:

    An entry like 1,1 -> 1,3 covers points 1,1, 1,2, and 1,3.
    An entry like 9,7 -> 7,7 covers points 9,7, 8,7, and 7,7.

For now, only consider horizontal and vertical lines: lines where either x1 = x2 or y1 = y2.

So, the horizontal and vertical lines from the above list would produce the following diagram:

.......1..
..1....1..
..1....1..
.......1..
.112111211
..........
..........
..........
..........
222111....

In this diagram, the top left corner is 0,0 and the bottom right corner is 9,9.
Each position is shown as the number of lines which cover that point or . if no line covers that point.
The top-left pair of 1s, for example, comes from 2,2 -> 2,1; the very bottom row is formed by the overlapping lines 0,9 -> 5,9 and 0,9 -> 2,9.

To avoid the most dangerous areas, you need to determine the number of points where at least two lines overlap.
In the above example, this is anywhere in the diagram with a 2 or larger - a total of 5 points.

Consider only horizontal and vertical lines.
At how many points do at least two lines overlap?
"""
from collections import namedtuple
from pathlib import Path
from typing import List

import numpy as np

Line = namedtuple("Line", ["x1", "y1", "x2", "y2"])


def load_lines_from_input(inputfile: Path) -> List[Line]:
    """Parse lines from input file."""
    lines = []
    for segment_text in inputfile.read_text().splitlines():
        (x1, y1), (x2, y2) = [coords.split(",") for coords in segment_text.split(" -> ")]
        lines.append(Line(int(x1), int(y1), int(x2), int(y2)))
    return lines


def create_grid_from_loaded_lines(lines: List[Line]) -> np.ndarray:
    """Create a grid of the appropriate size from loaded lines."""
    max_x = max(max(line.x1, line.x2) for line in lines)
    max_y = max(max(line.y1, line.y2) for line in lines)
    return np.zeros(shape=(max_x + 1, max_y + 1), dtype=int)


if __name__ == "__main__":
    lines = load_lines_from_input(Path("inputs.txt"))
    grid = create_grid_from_loaded_lines(lines)

    # Go through lines, add 1 to the relevant blocks in the grid
    for line in lines:
        if (line.x1 == line.x2) or (line.y1 == line.y2):  # horizontal or vertical lines
            if (line.x1 < line.x2) or (line.y1 < line.y2):  # left -> right or top -> bottom
                grid[line.x1 : line.x2 + 1, line.y1 : line.y2 + 1] += 1
            elif (line.x1 > line.x2) or (line.y1 > line.y2):  # right -> left or bottom -> top
                grid[line.x2 : line.x1 + 1, line.y2 : line.y1 + 1] += 1

    # Number of points with at least 2 lines overlapping -> value in grid is > 1
    print(np.count_nonzero(grid > 1))
