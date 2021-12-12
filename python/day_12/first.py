"""
--- Day 12: Passage Pathing ---

With your submarine's subterranean subsystems subsisting suboptimally, the only way you're getting out of this cave anytime soon 
is by finding a path yourself. 
Not just a path - the only way to know if you've found the best path is to find all of them.

Fortunately, the sensors are still mostly working, and so you build a rough map of the remaining caves (your puzzle input). 
For example:

start-A
start-b
A-c
A-b
b-d
A-end
b-end

This is a list of how all of the caves are connected. 
You start in the cave named start, and your destination is the cave named end. 
An entry like b-d means that cave b is connected to cave d - that is, you can move between them.

So, the above cave system looks roughly like this:

    start
    /   \
c--A-----b--d
    \   /
     end

Your goal is to find the number of distinct paths that start at start, end at end, and don't visit small caves more than once. 
There are two types of caves: big caves (written in uppercase, like A) and small caves (written in lowercase, like b). 
It would be a waste of time to visit any small cave more than once, but big caves are large enough that it might be worth visiting them multiple times. 
So, all paths you find should visit small caves at most once, and can visit big caves any number of times.

Given these rules, there are 10 paths through this example cave system:

start,A,b,A,c,A,end
start,A,b,A,end
start,A,b,end
start,A,c,A,b,A,end
start,A,c,A,b,end
start,A,c,A,end
start,A,end
start,b,A,c,A,end
start,b,A,end
start,b,end

(Each line in the above list corresponds to a single path; the caves visited by that path are listed in the order they are visited and separated by commas.)

Note that in this cave system, cave d is never visited by any path: to do so, cave b would need to be visited twice 
(once on the way to cave d and a second time when returning from cave d), and since cave b is small, this is not allowed.

Here is a slightly larger example:

dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc

The 19 paths through it are as follows:

start,HN,dc,HN,end
start,HN,dc,HN,kj,HN,end
start,HN,dc,end
start,HN,dc,kj,HN,end
start,HN,end
start,HN,kj,HN,dc,HN,end
start,HN,kj,HN,dc,end
start,HN,kj,HN,end
start,HN,kj,dc,HN,end
start,HN,kj,dc,end
start,dc,HN,end
start,dc,HN,kj,HN,end
start,dc,end
start,dc,kj,HN,end
start,kj,HN,dc,HN,end
start,kj,HN,dc,end
start,kj,HN,end
start,kj,dc,HN,end
start,kj,dc,end

Finally, this even larger example has 226 paths through it:

fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW

How many paths through this cave system are there that visit small caves at most once?
"""
from collections import defaultdict
from pathlib import Path
from typing import Dict, Set, Tuple


def construct_cave_map(inputfile: Path) -> Tuple[Dict[str, Set[str]], Set[str]]:
    """Provided with the input, maps which caves are connected to which and which caves are small."""
    connections = inputfile.read_text().splitlines()
    caves = defaultdict(set)  # will hold the list of connected caves for each cave
    small_caves = set()  # will hold the list of small caves, as they can only be visited once

    for line in connections:
        cave_from, cave_to = line.split("-")
        caves[cave_from].add(cave_to)  # register the connection (forward)
        caves[cave_to].add(cave_from)  # register the connection (backward)
        for cave in (cave_from, cave_to):
            if cave.islower():
                small_caves.add(cave)  # register the small caves
    return caves, small_caves


def find_paths(caves: Dict[str, Set[str]], small_caves: Set[str]) -> Set[Tuple[str, ...]]:
    """
    Provided with the cave map, finds all acceptable paths: goes from start to end, and at most
    once through small caves.
    """
    paths: Set[Tuple[str, ...]] = {("start",)}  # will store all unique paths
    while True:
        for path in [*paths]:
            if path[-1] == "end":  # this path is valid, let's leave it alone
                continue
            paths.remove(path)  # does not lead to the end, remove it
            unvisitable = {cave for cave in path if cave in small_caves}  # find the "unvisitable" caves
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
