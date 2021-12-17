"""
--- Day 17: Trick Shot ---

You finally decode the Elves' message. HI, the message says. 
You continue searching for the sleigh keys.

Ahead of you is what appears to be a large ocean trench. 
Could the keys have fallen into it? 
You'd better send a probe to investigate.

The probe launcher on your submarine can fire the probe with any integer velocity in the x (forward) and y (upward, or downward if negative) directions. 
For example, an initial x,y velocity like 0,10 would fire the probe straight up, while an initial velocity like 10,-1 would fire the probe forward 
at a slight downward angle.

The probe's x,y position starts at 0,0. Then, it will follow some trajectory by moving in steps. On each step, these changes occur in the following order:

    The probe's x position increases by its x velocity.
    The probe's y position increases by its y velocity.
    Due to drag, the probe's x velocity changes by 1 toward the value 0; that is, it decreases by 1 if it is greater than 0, increases by 1 if it is less than 0, or does not change if it is already 0.
    Due to gravity, the probe's y velocity decreases by 1.

For the probe to successfully make it into the trench, the probe must be on some trajectory that causes it to be within a target area after any step. 
The submarine computer has already calculated this target area (your puzzle input). 
For example:

target area: x=20..30, y=-10..-5

This target area means that you need to find initial x,y velocity values such that after any step, the probe's x position is at least 20 
and at most 30, and the probe's y position is at least -10 and at most -5.

Given this target area, one initial velocity that causes the probe to be within the target area after any step is 7,2:

.............#....#............
.......#..............#........
...............................
S........................#.....
...............................
...............................
...........................#...
...............................
....................TTTTTTTTTTT
....................TTTTTTTTTTT
....................TTTTTTTT#TT
....................TTTTTTTTTTT
....................TTTTTTTTTTT
....................TTTTTTTTTTT

In this diagram, S is the probe's initial position, 0,0. The x coordinate increases to the right, and the y coordinate increases upward. 
In the bottom right, positions that are within the target area are shown as T. 
After each step (until the target area is reached), the position of the probe is marked with #. 
(The bottom-right # is both a position the probe reaches and a position in the target area.)

Another initial velocity that causes the probe to be within the target area after any step is 6,3:

...............#..#............
...........#........#..........
...............................
......#..............#.........
...............................
...............................
S....................#.........
...............................
...............................
...............................
.....................#.........
....................TTTTTTTTTTT
....................TTTTTTTTTTT
....................TTTTTTTTTTT
....................TTTTTTTTTTT
....................T#TTTTTTTTT
....................TTTTTTTTTTT

Another one is 9,0:

S........#.....................
.................#.............
...............................
........................#......
...............................
....................TTTTTTTTTTT
....................TTTTTTTTTT#
....................TTTTTTTTTTT
....................TTTTTTTTTTT
....................TTTTTTTTTTT
....................TTTTTTTTTTT

One initial velocity that doesn't cause the probe to be within the target area after any step is 17,-4:

S..............................................................
...............................................................
...............................................................
...............................................................
.................#.............................................
....................TTTTTTTTTTT................................
....................TTTTTTTTTTT................................
....................TTTTTTTTTTT................................
....................TTTTTTTTTTT................................
....................TTTTTTTTTTT..#.............................
....................TTTTTTTTTTT................................
...............................................................
...............................................................
...............................................................
...............................................................
................................................#..............
...............................................................
...............................................................
...............................................................
...............................................................
...............................................................
...............................................................
..............................................................#

The probe appears to pass through the target area, but is never within it after any step. 
Instead, it continues down and to the right - only the first few steps are shown.

If you're going to fire a highly scientific probe out of a super cool probe launcher, you might as well do it with style. 
How high can you make the probe go while still reaching the target area?

In the above example, using an initial velocity of 6,9 is the best you can do, causing the probe to reach a maximum y position of 45. 
(Any higher initial y velocity causes the probe to overshoot the target area entirely.)

Find the initial velocity that causes the probe to reach the highest y position and still eventually be within the target area after any step. 
What is the highest y position it reaches on this trajectory?
"""
from math import sqrt
from pathlib import Path
from typing import List, Tuple


def parse_target_area(inputfile: Path) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """Parses the input data for the coordinates of the target area."""
    targets = inputfile.read_text().split()[2:]
    x0, x1 = targets[0].split("..")
    y0, y1 = targets[1].split("..")

    x0 = int(x0.strip("x="))  # remove the 'x=' part
    x1 = int(x1.strip(","))  # remove the trailing comma
    y0 = int(y0.strip("y="))  # remove the 'y=' part
    y1 = int(y1.strip(","))  # no trailing comma here but doesn't hurt

    return (x0, x1), (y0, y1)


def determine_extrema_starting_velocities(
    target_xs: Tuple[int, int], target_ys: Tuple[int, int]
) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """
    Determines the min/max starting velocities that will cause the probe to reach the target area, if possible.
    These will give us the seach space to go over.
    """
    # Min vx_0 to never undershoot : x_t_inf >= xmin => vx_0(vx_0+1)/2 >= xmin => vx_0 >= (sqrt(8*xmin+1)-1)/2
    min_velocity_x_0 = int((sqrt(8 * target_xs[0] + 1) - 1) / 2)

    # Max vx_0 to never overshoot: x_0 <= xmax => vx_0 <= xmax
    max_velocity_x_0 = target_xs[1]

    # Min vy_0 to never undershoot : y_t >= ymin => t*vy_0 - t*(t-1)/2 >= ymin
    min_velocity_y_0 = min(0, target_ys[0])

    # Max vy_0 : the part of the trajectory where y goes up is symmetric in y : we pass by the same y values going up / down
    # and also the y speed at each point is also symmetric. So, if y(t) = 0, we need y(t+1) >= ymin (assuming negative y target):
    # y(t_cross) = 0 => vy(t_cross) = -(vy(0)+1) => y(t_cross+1) >= ymin => -(vy(0)+1) >= ymin => vy(0) <= -ymin-1
    max_velocity_y_0 = -target_ys[0] - 1
    return (min_velocity_x_0, max_velocity_x_0), (min_velocity_y_0, max_velocity_y_0)


if __name__ == "__main__":
    target_xs, target_ys = parse_target_area(Path("inputs.txt"))
    (min_vx0, max_vx0), (min_vy0, max_vy0) = determine_extrema_starting_velocities(target_xs, target_ys)
    all_time_high = 0

    # Now we go over the trajectories we get from starting in this range of values that would all land in the target area
    for vx_0 in range(min_vx0, max_vx0 + 1):
        for vy_0 in range(min_vy0, max_vy0 + 1):
            x = y = trajectory_max_y = 0  # we initialize starting positions and max y of this trajectory
            vx = vx_0  # start with this initial x velocity
            vy = vy_0  # start with this initial y velocity
            while x <= target_xs[1] and y >= target_ys[0]:  # as long as we're not out of the target range
                x += vx  # 'the probe's x position increases by its x velocity'
                y += vy  # 'the probe's y position increases by its y velocity'
                vx = vx - 1 if vx > 0 else 0  # 'due to drag, the probe's x velocity changes by 1 toward the value 0'
                vy -= 1  # 'due to gravity, the probe's y velocity decreases by 1'
                trajectory_max_y = max(trajectory_max_y, y)

                # Check if we're in the target area, if so we can stop
                if target_xs[0] <= x <= target_xs[1] and target_ys[0] <= y <= target_ys[1]:
                    all_time_high = max(all_time_high, trajectory_max_y)  # update all time high
                    break

    print(all_time_high)
