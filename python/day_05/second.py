"""
--- Part Two ---

Unfortunately, considering only horizontal and vertical lines doesn't give you the full picture; you need to also 
consider diagonal lines.

Because of the limits of the hydrothermal vent mapping system, the lines in your list will only ever be horizontal, 
vertical, or a diagonal line at exactly 45 degrees. In other words:

    An entry like 1,1 -> 3,3 covers points 1,1, 2,2, and 3,3.
    An entry like 9,7 -> 7,9 covers points 9,7, 8,8, and 7,9.

Considering all lines from the above example would now produce the following diagram:

1.1....11.
.111...2..
..2.1.111.
...1.2.2..
.112313211
...1.2....
..1...1...
.1.....1..
1.......1.
222111....

You still need to determine the number of points where at least two lines overlap.
In the above example, this is still anywhere in the diagram with a 2 or larger - now a total of 12 points.

Consider all of the lines. 
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
    # Same as first part, more cases to consider
    lines = load_lines_from_input(Path("inputs.txt"))
    grid = create_grid_from_loaded_lines(lines)

    # Go through lines, add 1 to the relevant blocks in the grid
    for line in lines:
        if (line.x1 == line.x2) or (line.y1 == line.y2):  # horizontal or vertical lines
            if (line.x1 < line.x2) or (line.y1 < line.y2):  # left -> right or top -> bottom
                grid[line.x1 : line.x2 + 1, line.y1 : line.y2 + 1] += 1
            elif (line.x1 > line.x2) or (line.y1 > line.y2):  # right -> left or bottom -> top
                grid[line.x2 : line.x1 + 1, line.y2 : line.y1 + 1] += 1

        # ----- Part 2 ----- #
        elif (line.x1 != line.x2) and (line.y1 != line.y2):  # diagonal lines
            # Find out if coordinates are increasing or decreasing
            x_dir = -1 if line.x1 > line.x2 else 1
            y_dir = -1 if line.y1 > line.y2 else 1

            # Return coordinate pairs, with each coordinate changing one unit at a time
            # (according to whether it is increasing or decreasing)
            xy_range = zip(range(line.x1, line.x2 + x_dir, x_dir), range(line.y1, line.y2 + y_dir, y_dir))
            for x, y in xy_range:  # add one to each point
                grid[x, y] += 1

    # Number of points with at least 2 lines overlapping -> value in grid is > 1
    print(np.count_nonzero(grid > 1))
