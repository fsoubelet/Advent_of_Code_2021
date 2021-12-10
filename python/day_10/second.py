"""
--- Part Two ---

Now, discard the corrupted lines. 
The remaining lines are incomplete.

Incomplete lines don't have any incorrect characters - instead, they're missing some closing characters at the end of the line. 
To repair the navigation subsystem, you just need to figure out the sequence of closing characters that complete all open chunks in the line.

You can only use closing characters (), ], }, or >), and you must add them in the correct order so that only legal pairs 
are formed and all chunks end up closed.

In the example above, there are five incomplete lines:

    [({(<(())[]>[[{[]{<()<>> - Complete by adding }}]])})].
    [(()[<>])]({[<{<<[]>>( - Complete by adding )}>]}).
    (((({<>}<{<{<>}{[]{[]{} - Complete by adding }}>}>)))).
    {<[[]]>}<{[{[{[]{()[[[] - Complete by adding ]]}}]}]}>.
    <{([{{}}[<[[[<>{}]]]>[]] - Complete by adding ])}>.

Did you know that autocomplete tools also have contests? It's true! 
The score is determined by considering the completion string character-by-character. 
Start with a total score of 0, then for each character, multiply the total score by 5 and then increase 
the total score by the point value given for the character in the following table:

    ): 1 point.
    ]: 2 points.
    }: 3 points.
    >: 4 points.

So, the last completion string above - ])}> - would be scored as follows:

    Start with a total score of 0.
    Multiply the total score by 5 to get 0, then add the value of ] (2) to get a new total score of 2.
    Multiply the total score by 5 to get 10, then add the value of ) (1) to get a new total score of 11.
    Multiply the total score by 5 to get 55, then add the value of } (3) to get a new total score of 58.
    Multiply the total score by 5 to get 290, then add the value of > (4) to get a new total score of 294.

The five lines' completion strings have total scores as follows:

    }}]])})] - 288957 total points.
    )}>]}) - 5566 total points.
    }}>}>)))) - 1480781 total points.
    ]]}}]}]}> - 995444 total points.
    ])}> - 294 total points.

Autocomplete tools are an odd bunch: the winner is found by sorting all of the scores and then taking the middle score. 
(There will always be an odd number of scores to consider.) 
In this example, the middle score is 288957 because there are the same number of scores smaller and larger than it.

Find the completion string for each incomplete line, score the completion strings, and sort the scores. 
What is the middle score?
"""
from collections import deque
from pathlib import Path
from statistics import median

PAIRS = {"(": ")", "[": "]", "{": "}", "<": ">"}
SCORES = {")": 1, "]": 2, "}": 3, ">": 4}


def line_score(line: str) -> int:
    """
    Returns the score of a given line, which would be 0 if it is not corrupted.
    We solve using the fact that any closing character should match the opening character
    directly to its left, or the first opening character to its left once the valid pairs
    been removed.
    """
    queue = deque()  # will store expected characters

    for character in line:
        if character in PAIRS:  # opening character
            queue.append(PAIRS[character])  # put its "closing" partner in the queue, which we hope to find later
        elif character != queue[-1]:  #  as seen in part 1 -> corrupted line
            return 0  # return 0 as we don't care about corrupted lines here
        elif character == queue[-1]:  # closing character, and it matches the last one in the queue
            queue.pop()  # remove the expected character from the queue and consider that pair done

    # By this point, in the queue we have all expected closing characters that we not encountered
    # These are the characters that are missing from the line, and we calculate the score from them
    score = 0
    for character in reversed(queue):  # the order in which we added matters because of the multiplication!
        score *= 5
        score += SCORES[character]
    return score


if __name__ == "__main__":
    inputs = Path("inputs.txt").read_text().splitlines()
    line_scores = [line_score(line) for line in inputs]
    # Keep scores from incomplete lines only, don't keep 0s (corrupted lines scores) as it will affect the median
    non_zero_scores = [score for score in line_scores if score != 0]
    print(median(non_zero_scores))
