"""
--- Part Two ---

After reviewing the available paths, you realize you might have time to visit a single small cave twice. 
Specifically, big caves can be visited any number of times, a single small cave can be visited at most twice, and the remaining 
small caves can be visited at most once. 
However, the caves named start and end can only be visited exactly once each: once you leave the start cave, you may not return to it, 
and once you reach the end cave, the path must end immediately.

Now, the 36 possible paths through the first example above are:

start,A,b,A,b,A,c,A,end
start,A,b,A,b,A,end
start,A,b,A,b,end
start,A,b,A,c,A,b,A,end
start,A,b,A,c,A,b,end
start,A,b,A,c,A,c,A,end
start,A,b,A,c,A,end
start,A,b,A,end
start,A,b,d,b,A,c,A,end
start,A,b,d,b,A,end
start,A,b,d,b,end
start,A,b,end
start,A,c,A,b,A,b,A,end
start,A,c,A,b,A,b,end
start,A,c,A,b,A,c,A,end
start,A,c,A,b,A,end
start,A,c,A,b,d,b,A,end
start,A,c,A,b,d,b,end
start,A,c,A,b,end
start,A,c,A,c,A,b,A,end
start,A,c,A,c,A,b,end
start,A,c,A,c,A,end
start,A,c,A,end
start,A,end
start,b,A,b,A,c,A,end
start,b,A,b,A,end
start,b,A,b,end
start,b,A,c,A,b,A,end
start,b,A,c,A,b,end
start,b,A,c,A,c,A,end
start,b,A,c,A,end
start,b,A,end
start,b,d,b,A,c,A,end
start,b,d,b,A,end
start,b,d,b,end
start,b,end

The slightly larger example above now has 103 paths through it, and the even larger example now has 3509 paths through it.
Given these new rules, how many paths through this cave system are there?
"""
from collections import Counter
from pathlib import Path
from typing import Dict, Set, Tuple

from first import construct_cave_map


# Almost same as part 1 but we tweak the logic a bit
def find_paths(caves: Dict[str, Set[str]], small_caves: Set[str]) -> Set[Tuple[str, ...]]:
    """Provided with the cave map, finds all acceptable paths with new rules."""
    paths: Set[Tuple[str, ...]] = {("start",)}  # will store all unique paths
    while True:
        for path in [*paths]:
            if path[-1] == "end":  # this path is valid, let's leave it alone
                continue
            paths.remove(path)  # does not lead to the end, remove it
            small_cave_visits = Counter([cave for cave in path if cave in small_caves])

            # If a small cave has been visited twice, cannot visit small caves more than once now
            if 2 in small_cave_visits.values():
                unvisitable = {cave for cave in path if cave in small_caves}  # find the "unvisitable" caves
            else:
                unvisitable = {"start"}  # as per new rules

            for cave in caves[path[-1]] - unvisitable:  # for each cave that is connected to the last one, and visitable
                paths.add((*path, cave))
        if all([p[-1] == "end" for p in paths]):  # all remaining paths lead to the end
            break
    return paths


if __name__ == "__main__":
    inputfile = Path("inputs.txt")
    caves, small_caves = construct_cave_map(inputfile)
    paths = find_paths(caves, small_caves)
    print(len(paths))
