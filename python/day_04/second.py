"""
--- Part Two ---

On the other hand, it might be wise to try a different strategy: let the giant squid win.

You aren't sure how many bingo boards a giant squid could play at once, so rather than waste time counting its arms, 
the safe thing to do is to figure out which board will win last and choose that one.
That way, no matter which boards it picks, it will win for sure.

In the above example, the second board is the last to win, which happens after 13 is eventually called and its middle column is completely marked. 
If you were to keep playing until this point, the second board would have a sum of unmarked numbers equal to 148 for a final score of 148 * 13 = 1924.

Figure out which board will win last. Once it wins, what would its final score be?
"""
# This is exactly part 1 but we return the last winning sum instead of the first one
# Apart from the last line of code, this is identical to first.py

from pathlib import Path
from typing import List

import numpy as np


def read_random_numbers(inputfile: Path) -> np.ndarray:
    """Returns the random numbers (first line) from the input file as a numpy array of ints."""
    with inputfile.open("r") as f:
        return np.array(f.readline().split(","), dtype=int)


def read_bingo_boards(inputfile: Path) -> np.ndarray:
    """Returns an array with the bingo boards from the input file, each as a 5x5 numpy array of ints."""
    contents = inputfile.read_text().splitlines()
    boards_lists = [[int(n) for n in line.split()] for line in contents[1:] if line != ""]
    num_boards = len(boards_lists) // 5
    return np.array(boards_lists).reshape((num_boards, 5, 5))


def check_number_in_boards(number: int, boards: np.ndarray, marked_boards: np.ndarray) -> bool:
    """Checks the presence of `number` in the board, marks where it is in the dummies with a 1."""
    # Go through all positions in all boards, if number is found mark it with a 1 in the dummy boards.
    for z in range(boards.shape[0]):  # number of boards
        for y in range(5):  # lazy double loop to go through the board
            for x in range(5):
                if boards[z, y, x] == number:
                    marked_boards[z, y, x] = 1


def find_sum_of_board(boards: np.ndarray, marked_boards: np.ndarray, index: int, number: int) -> int:
    """
    Given the board at index `inde`, return its sum according to the elements marked on that board.

    Args:
        boards (np.ndarray): array of bingo boards, each a 5x5 np.ndarray
        marked_boards (np.ndarray): array of dummies, each a 5x5 np.ndarray with either 0 or 1 values
        index (int): index of the board to check
        number (int): the random number we are currently solving for
    """
    not_marked = []  # will hold all numbers not marked for the win
    for y in range(5):  # lazy double loop to go through the board
        for x in range(5):
            if not marked_boards[index, y, x]:  # position isn't marked with a 1
                not_marked.append(boards[index, y, x])
    return sum(not_marked) * number


# CAN GO TO MAIN
def check_for_winning_boards(
    boards: np.ndarray,
    marked_boards: np.ndarray,
    winner_boards: List[int],
    winning_sums: List[int],
    number: int,
) -> None:
    """
    Go through the 'marked' dummy boards, checks if there are winners.
    If a winner is found, the sum for the appropriate board is calculated and added to the list of sums.

    Args:
        boards (np.ndarray): array of bingo boards, each a 5x5 np.ndarray
        marked_boards (np.ndarray): array of dummies, each a 5x5 np.ndarray with either 0 or 1 values
        winner_boards (List[int]): list of indices of the winning boards
        winning_sums (List[int]): list of sums of the winning boards
        number (int): number we are currently indexing for
    """
    for index in range(marked_boards.shape[0]):  # number of boards
        if index in winner_boards:  # no need to check it again if it's already a winner
            continue
        else:
            # Sum across both axes: if there is a 5 in the result, one of these axes is full of 1s so the board is a winner
            if (5 in np.sum(marked_boards[index], axis=0)) or (5 in np.sum(marked_boards[index], axis=1)):
                winner_boards.append(index)
                winning_sums.append(find_sum_of_board(boards, marked_boards, index, number))


if __name__ == "__main__":
    inputs_file = Path("inputs.txt")
    random_numbers = read_random_numbers(inputs_file)
    bingo_boards = read_bingo_boards(inputs_file)

    # Setting up the variables needed.
    marked = np.zeros(bingo_boards.shape, dtype=int)  # blank canvas, change values to 1 when marked
    winner_boards = []
    winning_sums = []

    for number in random_numbers:
        check_number_in_boards(number, bingo_boards, marked)
        check_for_winning_boards(bingo_boards, marked, winner_boards, winning_sums, number)
    print(winning_sums[-1])  # sum for the last winning board to be found
