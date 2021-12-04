"""--- Day 4: Giant Squid ---

You're already almost 1.5km (almost a mile) below the surface of the ocean, already so deep that you can't see any sunlight.
What you can see, however, is a giant squid that has attached itself to the outside of your submarine.

Maybe it wants to play bingo?

Bingo is played on a set of boards each consisting of a 5x5 grid of numbers.
Numbers are chosen at random, and the chosen number is marked on all boards on which it appears. (Numbers may not appear on all boards.)
If all numbers in any row or any column of a board are marked, that board wins. (Diagonals don't count.)

The submarine has a bingo subsystem to help passengers (currently, you and the giant squid) pass the time.
It automatically generates a random order in which to draw numbers and a random set of boards (your puzzle input).
For example:

7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7

After the first five numbers are drawn (7, 4, 9, 5, and 11), there are no winners, but the boards are 
marked as follows (shown here adjacent to each other to save space):

22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
 8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
 6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
 1 12 20 15 19        14 21 16 12  6         2  0 12  3  7

After the next six numbers are drawn (17, 23, 2, 0, 14, and 21), there are still no winners:

22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
 8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
 6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
 1 12 20 15 19        14 21 16 12  6         2  0 12  3  7

Finally, 24 is drawn:

22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
 8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
 6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
 1 12 20 15 19        14 21 16 12  6         2  0 12  3  7

At this point, the third board wins because it has at least one complete row or column of marked 
numbers (in this case, the entire top row is marked: 14 21 17 24 4).

The score of the winning board can now be calculated. Start by finding the sum of all unmarked numbers on that board; in this case, the sum is 188. 
Then, multiply that sum by the number that was just called when the board won, 24, to get the final score, 188 * 24 = 4512.

To guarantee victory against the giant squid, figure out which board will win first. 
What will your final score be if you choose that board?
"""
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
    print(winning_sums[0])  # sum for the first winning board to be found
