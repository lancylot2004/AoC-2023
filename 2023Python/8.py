from math import lcm
import re

from template import getLines, timeAvgAndPrint

PATTERN = r"([A-Z0-9]{3}) = \(([A-Z0-9]{3}), ([A-Z0-9]{3})\)"

def parseMap():
    lines = getLines(8)
    inst = next(lines).strip()
    next(lines)

    nodes = [re.findall(PATTERN, line.strip())[0] for line in lines]
    nodes = {node[0]: (node[1], node[2]) for node in nodes}
    return inst, nodes

# === Part One ===
def partOne(inst, nodes):
    steps = 0
    currNode = "AAA"

    while currNode != "ZZZ":
        currNode = nodes[currNode][0] if inst[steps % len(inst)] == 'L' else nodes[currNode][1]
        steps += 1
    
    return steps

# === Part Two ===
def partTwo(inst, nodes):
    aNodes = [key for key in nodes.keys() if key.endswith('A')]
    cycleLengths = []

    for aNode in aNodes:
        tmpSteps = 0
        currNode = aNode
        while not currNode.endswith('Z'):
            currNode = nodes[currNode][0] if inst[tmpSteps % len(inst)] == 'L' else nodes[currNode][1]
            tmpSteps += 1
        cycleLengths.append(tmpSteps)
    
    return lcm(*cycleLengths)

if __name__ == "__main__":
    inst, nodes = parseMap()

    timeAvgAndPrint("Part One", 100, partOne, inst, nodes)
    timeAvgAndPrint("Part Two", 100, partTwo, inst, nodes)