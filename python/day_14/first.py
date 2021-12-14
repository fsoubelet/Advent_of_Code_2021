"""
--- Day 14: Extended Polymerization ---

The incredible pressures at this depth are starting to put a strain on your submarine. 
The submarine has polymerization equipment that would produce suitable materials to reinforce the submarine, and the nearby 
volcanically-active caves should even have the necessary input elements in sufficient quantities.

The submarine manual contains instructions for finding the optimal polymer formula; specifically, it offers a polymer 
template and a list of pair insertion rules (your puzzle input). 
You just need to work out what polymer would result after repeating the pair insertion process a few times.

For example:

NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C

The first line is the polymer template - this is the starting point of the process.

The following section defines the pair insertion rules. 
A rule like AB -> C means that when elements A and B are immediately adjacent, element C should be inserted between them. 
These insertions all happen simultaneously.

So, starting with the polymer template NNCB, the first step simultaneously considers all three pairs:

    The first pair (NN) matches the rule NN -> C, so element C is inserted between the first N and the second N.
    The second pair (NC) matches the rule NC -> B, so element B is inserted between the N and the C.
    The third pair (CB) matches the rule CB -> H, so element H is inserted between the C and the B.

Note that these pairs overlap: the second element of one pair is the first element of the next pair. 
Also, because all pairs are considered simultaneously, inserted elements are not considered to be part of a pair until the next step.

After the first step of this process, the polymer becomes NCNBCHB.

Here are the results of a few steps using the above rules:

Template:     NNCB
After step 1: NCNBCHB
After step 2: NBCCNBBBCBHCB
After step 3: NBBBCNCCNBBNBNBBCHBHHBCHB
After step 4: NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB

This polymer grows quickly. After step 5, it has length 97; After step 10, it has length 3073. 
After step 10, B occurs 1749 times, C occurs 298 times, H occurs 161 times, and N occurs 865 times; 
taking the quantity of the most common element (B, 1749) and subtracting the quantity of the least common element (H, 161) produces 1749 - 161 = 1588.

Apply 10 steps of pair insertion to the polymer template and find the most and least common elements in the result. 
What do you get if you take the quantity of the most common element and subtract the quantity of the least common element?
"""
from collections import Counter
from pathlib import Path
from typing import Dict, Tuple


def parse_input(inputfile: Path) -> Tuple[str, Dict[str, str]]:
    """Extracts the initial sequence and the rules from the input file."""
    sequence, _, *rules = inputfile.read_text().splitlines()
    rules = dict(rule.split(" -> ") for rule in rules)
    return sequence, rules


def grow_polymer(polymer: str, rules: Dict[str, str], nsteps: int) -> Counter:
    """Grow the polymer_sequence nsteps times according to the rules, returns counts of elements."""
    # Instantiate counts of elements and pairs
    element_counts = Counter(polymer)
    pair_counts = Counter(polymer[i : i + 2] for i in range(len(polymer) - 1))

    for step in range(nsteps):
        new_count = Counter()
        for pair, num in pair_counts.items():  # let's apply the rules to each pair
            if pair in rules:
                a, b = pair
                c = rules[pair]
                # Number of insertions of C is the number of AB pairs since it goes between A and B
                new_count[a + c] += num  # first count AC from ACB
                new_count[c + b] += num  # then count CB from ACB
                element_counts[c] += num  # update the amount of Cs
            else:
                new_count[pair] += num  # the pair hasn't changed
            pair_counts = new_count  # update the pair counts
    return element_counts


if __name__ == "__main__":
    sequence, rules = parse_input(Path("inputs.txt"))
    element_counts = grow_polymer(sequence, rules, 10)  # we do 10 steps in part 1
    print(max(element_counts.values()) - min(element_counts.values()))
