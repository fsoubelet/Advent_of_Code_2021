"""
--- Part Two ---

Next, you should verify the life support rating, which can be determined by multiplying the oxygen generator rating by
the CO2 scrubber rating.

Both the oxygen generator rating and the CO2 scrubber rating are values that can be found in your diagnostic 
report - finding them is the tricky part.
Both values are located using a similar process that involves filtering out values until only one remains.
Before searching for either rating value, start with the full list of binary numbers from your diagnostic 
report and consider just the first bit of those numbers.
Then:

    Keep only numbers selected by the bit criteria for the type of rating value for which you are searching.
    Discard numbers which do not match the bit criteria.
    If you only have one number left, stop; this is the rating value for which you are searching.
    Otherwise, repeat the process, considering the next bit to the right.

The bit criteria depends on which type of rating value you want to find:

    To find oxygen generator rating, determine the most common value (0 or 1) in the current bit position, and keep only numbers with that bit in that position.
    If 0 and 1 are equally common, keep values with a 1 in the position being considered.
    To find CO2 scrubber rating, determine the least common value (0 or 1) in the current bit position, and keep only numbers with that bit in that position.
    If 0 and 1 are equally common, keep values with a 0 in the position being considered.

For example, to determine the oxygen generator rating value using the same example diagnostic report from above:

    Start with all 12 numbers and consider only the first bit of each number.
    There are more 1 bits (7) than 0 bits (5), so keep only the 7 numbers with a 1 in the first position: 11110, 10110, 10111, 10101, 11100, 10000, and 11001.
    Then, consider the second bit of the 7 remaining numbers: there are more 0 bits (4) than 1 bits (3), so keep only the 4 numbers with a 0 in the second position: 10110, 10111, 10101, and 10000.
    In the third position, three of the four numbers have a 1, so keep those three: 10110, 10111, and 10101.
    In the fourth position, two of the three numbers have a 1, so keep those two: 10110 and 10111.
    In the fifth position, there are an equal number of 0 bits and 1 bits (one each). So, to find the oxygen generator rating, keep the number with a 1 in that position: 10111.
    As there is only one number left, stop; the oxygen generator rating is 10111, or 23 in decimal.

Then, to determine the CO2 scrubber rating value from the same example above:

    Start again with all 12 numbers and consider only the first bit of each number.
    There are fewer 0 bits (5) than 1 bits (7), so keep only the 5 numbers with a 0 in the first position: 00100, 01111, 00111, 00010, and 01010.
    Then, consider the second bit of the 5 remaining numbers: there are fewer 1 bits (2) than 0 bits (3), so keep only the 2 numbers with a 1 in the 
    second position: 01111 and 01010.
    In the third position, there are an equal number of 0 bits and 1 bits (one each). So, to find the CO2 scrubber rating, keep the number 
    with a 0 in that position: 01010.
    As there is only one number left, stop; the CO2 scrubber rating is 01010, or 10 in decimal.

Finally, to find the life support rating, multiply the oxygen generator rating (23) by the CO2 scrubber rating (10) to get 230.

Use the binary numbers in your diagnostic report to calculate the oxygen generator rating and CO2 scrubber rating, then multiply them together.
What is the life support rating of the submarine? (Be sure to represent your answer in decimal, not binary.)
"""
from copy import deepcopy
from pathlib import Path

import pandas as pd


def find_oxygen_rating(inputs: pd.DataFrame) -> int:
    df = deepcopy(inputs)
    column_position = 0

    while len(df) > 1:
        # We sum 0 or 1 values so if result > len/2, we had more 1s than len/2 elements so more than 0
        most_common_in_kth_place = 1 if df.loc[:, column_position].sum() >= len(df) / 2 else 0
        df = df[df.loc[:, column_position] == most_common_in_kth_place]  # keep those fitting the condition
        column_position += 1  # move to next position in the bits

    # Now we are left with a dataframe of only one row, just need to assemble it back to bits and then int
    oxygen_rating_bits = "".join(
        df.astype(str).to_numpy()[0]
    )  # result bits as a numpy array cast to a string
    return int(oxygen_rating_bits, 2)  # convert to int before returning


def find_co2_scrubber_rating(inputs: pd.DataFrame) -> int:
    df = deepcopy(inputs)
    column_position = 0

    while len(df) > 1:
        # same logic as find_oxygen_rating but flip the comparison to only keep least common bits
        least_common_in_kth_place = 1 if df.loc[:, column_position].sum() < len(df) / 2 else 0
        df = df[df.loc[:, column_position] == least_common_in_kth_place]  # keep those fitting the condition
        column_position += 1  # move to next position in the bits

    # Now we are left with a dataframe of only one row, just need to assemble it back to bits and then int
    co2_scrubber_rating_bits = "".join(
        df.astype(str).to_numpy()[0]
    )  # result bits as a numpy array cast to a string
    return int(co2_scrubber_rating_bits, 2)  # convert to int before returning


if __name__ == "__main__":
    # Read inputs as a list of lists, each element is a bit as string
    inputs = [list(line) for line in Path("inputs.txt").read_text().splitlines()]
    inputs = pd.DataFrame(inputs).astype(int)  # convert to pandas dataframe

    oxygen_rating = find_oxygen_rating(inputs)
    co2_scrubber_rating = find_co2_scrubber_rating(inputs)
    print(oxygen_rating * co2_scrubber_rating)
