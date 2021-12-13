"""
--- Part Two ---

Finish folding the transparent paper according to the instructions.
The manual says the code is always eight capital letters.

What code do you use to activate the infrared thermal imaging camera system?
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from first import construct_manual_page, parse_input


# It turns out my implementation for part 1 does not take in account the possible case where both halves
# during the folding have different dimensions, which was fine for my first fold but not the others.
# This implementation does.
def fold_array(array: np.ndarray, axis: str, index: int) -> np.ndarray:
    """Folds the array in the right place (axis, index) and return the new version with updated dots."""
    # We will slice the paper into two sections and flip
    if axis == "x":
        back = array[:index, :].copy()
        front = array[index + 1 :, :].copy()
        # We check the cases where both halves don't have the same dimensions and can't overlap
        if len(back[0]) > len(front[0]):  # front half is too small, we need to add a row
            front = np.hstack((front, np.zeros((len(back), len(back[0]) - len(front[0])))))  # zero pad it
        elif len(front[0]) > len(back[0]):  # back half is too small, we need to add a row
            back = np.hstack((np.zeros((len(front), len(front[0]) - len(back[0]))), back))  # zero pad it
        folded = np.flip(front, axis=0) + back

    elif axis == "y":
        back = array[:, :index].copy()
        front = array[:, index + 1 :].copy()
        # Check for the dimensions again, same logic
        if len(back[0]) > len(front[0]):
            front = np.hstack((front, np.zeros((len(back), len(back[0]) - len(front[0])))))
        elif len(front[0]) > len(back[0]):
            back = np.hstack((np.zeros((len(front), len(front[0]) - len(back[0]))), back))
        folded = np.flip(front, axis=1) + back
    return np.where(folded > 1, 1, folded)  # since overlapping dots count as one, values higher than 1 stay 1


if __name__ == "__main__":
    puzzle_input = Path("inputs.txt")
    dots, folds = parse_input(puzzle_input)
    manual_page = construct_manual_page(dots)

    # In part 2 we do all the folds
    for fold in folds:
        manual_page = fold_array(manual_page, fold[0], int(fold[1]))

    # Display the final grid, transposed here in my case
    plt.imshow(manual_page.T)
    plt.show()
