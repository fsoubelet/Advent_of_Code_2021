"""
--- Part Two ---

Through a little deduction, you should now be able to determine the remaining digits. 
Consider again the first example above:

acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab |
cdfeb fcadb cdfeb cdbaf

After some careful analysis, the mapping between signal wires and segments only make sense in the following configuration:

 dddd
e    a
e    a
 ffff
g    b
g    b
 cccc

So, the unique signal patterns would correspond to the following digits:

    acedgfb: 8
    cdfbe: 5
    gcdfa: 2
    fbcad: 3
    dab: 7
    cefabd: 9
    cdfgeb: 6
    eafb: 4
    cagedb: 0
    ab: 1

Then, the four digits of the output value can be decoded:

    cdfeb: 5
    fcadb: 3
    cdfeb: 5
    cdbaf: 3

Therefore, the output value for this entry is 5353.

Following this same process for each entry in the second, larger example above, the output value of each entry can be determined:

    fdgacbe cefdb cefbgd gcbe: 8394
    fcgedb cgb dgebacf gc: 9781
    cg cg fdcagb cbg: 1197
    efabcd cedba gadfec cb: 9361
    gecf egdcabf bgf bfgea: 4873
    gebdcfa ecba ca fadegcb: 8418
    cefg dcbef fcge gbcadfe: 4548
    ed bcgafe cdgba cbgef: 1625
    gbdfcae bgc cg cgb: 8717
    fgae cfgab fg bagce: 4315

Adding all of the output values in this larger example produces 61229.

For each entry, determine all of the wire/segment connections and decode the four-digit output values. 
What do you get if you add up all of the output values?
"""
# Note: the digits segments need to be turned on but not in a specific order, so for instance 'cfbegad' and 'fdgacbe' are the same digit.
# To circumvent this, let's use sets and frozensets when manipulating the digits, to take order out of the equation, and because these are
# hashable so I can use them in mappings
from pathlib import Path
from typing import Dict, List, Tuple


def deduce_pattern(patterns: List[Tuple[frozenset, int]]) -> Dict[str, str]:
    """
    Given a parsed input line, deduces the pattern and returns the determined mapping of pattern -> digit.
    So, taking the first example from the challenge, this function would return:
    {
        "acedgfb": "8", "cdfbe": "5", "gcdfa": "2", "fbcad": "3", "dab": "7",
        "cefabd": "9", "cdfgeb": "6", "eafb": "4", "cagedb": "0", "ab": "1"
    }
    """
    pattern_to_digit = {}

    # Let's start by those that are unique
    for pattern_frozenset, pattern_length in patterns:
        if pattern_length == 2:  # this can only be 1
            pattern_to_digit[pattern_frozenset] = "1"
        elif pattern_length == 3:  # this can only be 7
            pattern_to_digit[pattern_frozenset] = "7"
        elif pattern_length == 4:  # this can only be 4
            pattern_to_digit[pattern_frozenset] = "4"
        elif pattern_length == 7:  # this can only be 8
            pattern_to_digit[pattern_frozenset] = "8"

    # Let's reverse this mapping as I will need to do inverse lookups
    digit_to_pattern = {value: key for key, value in pattern_to_digit.items()}

    # Now let's try to find the rest, remaining patterns are for 2, 3, and 5 with a length of 5; and 0, 6 and 9 with a length of 6
    # ----- ----- ----- ----- -----
    # First case: distinguishing between 2, 3 and 5 if our pattern has 5 digits
    #  i. The digit 3 is the only one of those that has exactly 2 segments in common with 1, so if the pattern we are looking at contains the same letters contained in the pattern for 1, we just found the pattern for 3.
    #  ii. Otherwise, 5 is the only one of 2 and 5 which has exactly 3 segments in common with 4, so if the pattern we are looking at contains 3 letters that are also contained in the pattern for 4, we just fount the pattern for 5.
    #  iii. Otherwise, it has to be the pattern for 2
    # ----- ----- ----- ----- -----
    # Second case: distinguishing between 0, 6 and 9 if our pattern has 7 digits
    #  i. 9 is the only one to have 4 segments in common with 4
    #  ii. 6 is the only one to have 2 segments in common with 7.
    #  iii. If we didn't fill these conditions, we've found 0
    # ----- ----- ----- ----- -----
    # To check these conditions we'll make use of the .intersection() method of our frozensets, very convenient (binary operator &)
    for pattern_frozenset, pattern_length in patterns:
        if pattern_frozenset in pattern_to_digit:  # we've already solved this one
            continue
        elif pattern_length == 5:  # this is 2, 3 or 5
            if len(pattern_frozenset & digit_to_pattern["1"]) == 2:  # 2 segments in common with 1, this is a 3
                pattern_to_digit[pattern_frozenset] = "3"
            elif len(pattern_frozenset & digit_to_pattern["4"]) == 3:  # 3 segments in common with 4, this is a 5
                pattern_to_digit[pattern_frozenset] = "5"
            else:  # this has to be a 2
                pattern_to_digit[pattern_frozenset] = "2"
        else:  # this is 0, 6 and 9
            if len(pattern_frozenset & digit_to_pattern["4"]) == 4:  # 4 segments in common with 4, this is a 9
                pattern_to_digit[pattern_frozenset] = "9"
            elif len(pattern_frozenset & digit_to_pattern["7"]) == 2:  # 2 segments in common with 7, this is a 6
                pattern_to_digit[pattern_frozenset] = "6"
            else:  # this has to be a 0
                pattern_to_digit[pattern_frozenset] = "0"

    return pattern_to_digit


def solve_line(line: str) -> int:
    """Given a line of input, solves the wires mixup and returns the correct output value from the output digits."""
    raw_patterns, raw_output_digits = map(str.split, line.split("|"))
    patterns = [(frozenset(pattern), len(pattern)) for pattern in raw_patterns]
    output_digits = [(frozenset(digit), len(digit)) for digit in raw_output_digits]

    pattern_to_digit = deduce_pattern(patterns)
    # We concatenate the output digits together to see what number they represent and return that number
    output_value_string = "".join(pattern_to_digit[output_digit[0]] for output_digit in output_digits)
    return int(output_value_string)


if __name__ == "__main__":
    total_sum = 0
    for line in Path("inputs.txt").read_text().splitlines():
        total_sum += solve_line(line)
    print(total_sum)
