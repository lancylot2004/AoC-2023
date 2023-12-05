from intervaltree import IntervalTree, Interval
from itertools import chain
import re

SEED_PATTERN = r"seeds:(.*)"
MAP_TITLE_PATTERN = r"(\w*)-to-(\w*)"
MAP_PATTERN = r""

def parseMaps(path):
    with open(path, 'r') as file:
        # Extract initial seeds.
        initSeeds = [int(seed) for seed in re.findall(SEED_PATTERN, next(file))[0].strip().split(' ')]
        parseNew = False

        maps, orig, dest = {}, "", ""

        for line in file:
            # Check flag, and set current orig and dest if needed.
            if parseNew:
                orig, dest = re.findall(MAP_TITLE_PATTERN, line)[0]
                maps[(orig, dest)] = IntervalTree()
                parseNew = False
                continue

            # When new line, prepare for next map
            if line == '\n': 
                parseNew = True
                continue

            # In the absence of flags, add values to current map.
            destStart, origStart, howMany = [int(val) for val in line.strip().split(' ')]
            origEnd = origStart + howMany - 1
            destEnd = destStart + howMany - 1
            maps[(orig, dest)].addi(origStart, origEnd + 1, (destStart, destEnd))

        return initSeeds, maps

def findNextAttrib(currAttrib, maps):
    """Finds the next item in the 'chain' of attributes in the map."""
    for key in maps.keys():
        if key[0] == currAttrib:
            return key[1]
    return "Cheeky"

# === Part One ===
def mapValue(seed, tree):
    destInt = tree.at(seed)
    if len(destInt) > 0:
        destInt = destInt.pop()
        return destInt.data[0] + (seed - destInt.begin)
    
    return seed
        
def partOne(initSeeds, maps):
    # `initSeeds` will be overloaded to store current attributes.
    currOrig, currDest = "seed", findNextAttrib("seed", maps)
    
    while currDest != "location":
        for ind, seed in enumerate(initSeeds):
            initSeeds[ind] = mapValue(seed, maps[(currOrig, currDest)])
                        
        currOrig, currDest = currDest, findNextAttrib(currDest, maps)
        
    return min([mapValue(origVal, maps[(currOrig, currDest)]) for origVal in initSeeds])

# === Part Two ===
def initSeedToRange(initSeeds):
    seedTree = IntervalTree()
    
    # Showing off the most unnecessary Python syntax ever ~
    for seedFrom, howMany in zip(*[iter(initSeeds)] * 2):
        seedTree.addi(seedFrom, seedFrom + howMany)
        
    return seedTree

def partialIntr(tree1, tree2):
    intrs = []
    for interval1 in tree1:
        for interval2 in tree2:
            # Calculate the overlap
            start = max(interval1[0], interval2[0])
            end = min(interval1[1], interval2[1])
            if start < end:  # Ensuring there is an actual overlap
                intrs.append((start, end))
    return IntervalTree.from_tuples(intrs)

def partialDiff(fromTree, ofTree):
    difference = []
    for interval1 in fromTree:
        start, end = interval1.begin, interval1.end
        for interval2 in ofTree:
            if interval2.begin <= start < interval2.end:
                start = interval2.end  # Adjust the start to exclude the overlapping part
            elif interval2.begin < end <= interval2.end:
                end = interval2.begin  # Adjust the end to exclude the overlapping part
                
        # Add the non-overlapping part, if it exists
        if start + 1 < end:
            difference.append((start + 1, end))
    return difference

def mapRange(fromTree, toTree):
    intrs = partialIntr(fromTree, toTree)
    defRanges = partialDiff(toTree, intrs)
    mappedTree = IntervalTree()
    
    for mapInterval in intrs:
        for usingInterval in fromTree:
            if mapInterval.overlaps(usingInterval):
                intBegin = usingInterval.data[0] + (mapInterval.begin - usingInterval.begin)
                mappedTree.addi(intBegin, intBegin + mapInterval.length())
                
    for defInterval in defRanges:
        mappedTree.addi(defInterval[0], defInterval[1])
    
    return mappedTree


def partTwo(seedTree, maps):
    currOrig, currDest = "seed", findNextAttrib("seed", maps)
    
    while currOrig != "location":
        seedTree = mapRange(maps[(currOrig, currDest)], seedTree)
        currOrig, currDest = currDest, findNextAttrib(currDest, maps)
        
    # Find the minimum value directly from the seedTree
    return min(interval.begin for interval in seedTree if interval.begin != 0)


if __name__ == "__main__":
    initSeeds, maps = parseMaps("input.txt")
    print(partOne(initSeeds, maps))
    
    initSeeds, maps = parseMaps("input.txt")
    seedTrees = initSeedToRange(initSeeds)
    print(partTwo(seedTrees, maps))