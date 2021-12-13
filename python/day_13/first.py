"""
--- Day 13: Transparent Origami ---

You reach another volcanically active part of the cave.
It would be nice if you could do some kind of thermal imaging so you could tell ahead of time which caves are too hot to safely enter.

Fortunately, the submarine seems to be equipped with a thermal camera! When you activate it, you are greeted with:

Congratulations on your purchase! To activate this infrared thermal imaging
camera system, please enter the code found on page 1 of the manual.

Apparently, the Elves have never used this feature. To your surprise, you manage to find the manual; as you go to open it, page 1 falls out. 
It's a large sheet of transparent paper! The transparent paper is marked with random dots and includes instructions on how to fold it up (your puzzle input). 
For example:

6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5

The first section is a list of dots on the transparent paper. 0,0 represents the top-left coordinate. The first value, x, increases to the right. 
The second value, y, increases downward. So, the coordinate 3,0 is to the right of 0,0, and the coordinate 0,7 is below 0,0. 
The coordinates in this example form the following pattern, where # is a dot on the paper and . is an empty, unmarked position:

...#..#..#.
....#......
...........
#..........
...#....#.#
...........
...........
...........
...........
...........
.#....#.##.
....#......
......#...#
#..........
#.#........

Then, there is a list of fold instructions. 
Each instruction indicates a line on the transparent paper and wants you to fold the paper up (for horizontal y=... lines) 
or left (for vertical x=... lines). 
In this example, the first fold instruction is fold along y=7, which designates the line formed by all of the positions where y is 7 (marked here with -):

...#..#..#.
....#......
...........
#..........
...#....#.#
...........
...........
-----------
...........
...........
.#....#.##.
....#......
......#...#
#..........
#.#........

Because this is a horizontal line, fold the bottom half up. 
Some of the dots might end up overlapping after the fold is complete, but dots will never appear exactly on a fold line. 
The result of doing this fold looks like this:

#.##..#..#.
#...#......
......#...#
#...#......
.#.#..#.###
...........
...........

Now, only 17 dots are visible.

Notice, for example, the two dots in the bottom left corner before the transparent paper is folded; after the fold is complete, 
those dots appear in the top left corner (at 0,0 and 0,1). 
Because the paper is transparent, the dot just below them in the result (at 0,3) remains visible, as it can be seen through the transparent paper.

Also notice that some dots can end up overlapping; in this case, the dots merge together and become a single dot.

The second fold instruction is fold along x=5, which indicates this line:

#.##.|#..#.
#...#|.....
.....|#...#
#...#|.....
.#.#.|#.###
.....|.....
.....|.....

Because this is a vertical line, fold left:

#####
#...#
#...#
#...#
#####
.....
.....

The instructions made a square!

The transparent paper is pretty big, so for now, focus on just completing the first fold. 
After the first fold in the example above, 17 dots are visible - dots that end up overlapping after the fold is completed count as a single dot.

How many dots are visible after completing just the first fold instruction on your transparent paper?
"""
from pathlib import Path
from typing import List, Tuple

import numpy as np


def parse_input(filename: Path) -> Tuple[List[Tuple[int, int]], List[Tuple[str, int]]]:
    """
    Parses the input file and returns the list of dot coordinates as well as the list of folds.
    Each element in the list of folds holds the axis and position of the fold.
    """
    dots, folds = [], []
    puzzle_lines = filename.read_text().splitlines()
    for line in puzzle_lines:
        if line.startswith("fold"):  # it is an instruction line
            folds.append(line.split(" ")[-1].split("="))  # tuple with the axis and the number, for ex (x, 5)
        else:
            dots.append(line)
    dots = [(int(x.split(",")[0]), int(x.split(",")[1])) for x in dots if x != ""]
    folds = list(map(tuple, folds))
    return dots, folds


def construct_manual_page(dots: List[Tuple[int, int]]) -> np.ndarray:
    """Constructs the page from the dots positions. Dots are indicated with a 1, other positions with a 0."""
    x_max = max([x for x, _ in dots])
    y_max = max([y for _, y in dots])
    page = np.zeros((x_max + 1, y_max + 1), dtype=int)
    for coordinate in dots:
        page[coordinate] = 1
    return page


def fold_array(array: np.ndarray, axis: str, index: int) -> np.ndarray:
    """Folds the array in the right place (axis, index) and return the new version with updated dots."""
    # We will slice the paper into two sections and flip
    if axis == "x":
        back = array[:index, :].copy()
        front = array[index + 1 :, :].copy()
        folded = np.flip(front, axis=0) + back
    elif axis == "y":
        back = array[:, :index].copy()
        front = array[:, index + 1 :].copy()
        folded = np.flip(front, axis=1) + back
    return np.where(folded > 1, 1, folded)  # since overlapping dots count as one, values higher than 1 stay 1


if __name__ == "__main__":
    puzzle_input = Path("inputs.txt")
    dots, folds = parse_input(puzzle_input)
    manual_page = construct_manual_page(dots)

    # In part 1 we only do the first fold
    fold_axis, fold_index = folds[0]
    manual_page = fold_array(manual_page, axis=fold_axis, index=int(fold_index))
    print(np.sum(manual_page))  # number of dots is the number of 1s in our folded page
