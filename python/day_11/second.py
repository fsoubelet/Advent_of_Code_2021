"""
--- Part Two ---

It seems like the individual flashes aren't bright enough to navigate. 
However, you might have a better option: the flashes seem to be synchronizing!

In the example above, the first time all octopuses flash simultaneously is step 195:

After step 193:
5877777777
8877777777
7777777777
7777777777
7777777777
7777777777
7777777777
7777777777
7777777777
7777777777

After step 194:
6988888888
9988888888
8888888888
8888888888
8888888888
8888888888
8888888888
8888888888
8888888888
8888888888

After step 195:
0000000000
0000000000
0000000000
0000000000
0000000000
0000000000
0000000000
0000000000
0000000000
0000000000

If you can calculate the exact moments when the octopuses will all flash simultaneously, you should be able to navigate through the cavern. 
What is the first step during which all octopuses flash?
"""
import numpy as np
from first import count_step_flashes  # let's get this from part 1

if __name__ == "__main__":
    energy_levels = np.genfromtxt("inputs.txt", delimiter=1, dtype=int)
    steps = 0

    while True:
        steps += 1
        _ = count_step_flashes(energy_levels)  # this modifies energy levels accordingly

        if np.sum(energy_levels) == 0:  # all levels have been reset to 0, so everyone flashed that step!
            break

    print(steps)
