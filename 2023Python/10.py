from collections import deque
from typing import Generator
import numpy as np
import re
import shapely

from template import getLines, timeAndPrint, timeAvgAndPrint

OFFSETS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
PATTERN = r"F-*?J|J-*?F|L-*?7|7-*?L"

def parseGrid():
    lines = list(getLines(10))
    return np.array([[char for char in line.strip()] for line in lines])

def findStart(grid):
    start = np.where(grid == 'S')
    return (start[1][0], start[0][0])

inBound = lambda x, y, grid: 0 <= x < grid.shape[1] and 0 <= y < grid.shape[0]

def getNextCoords(grid, x, y):
    if not inBound(x, y, grid): return []
    match grid[y, x]:
        case 'S':
            global OFFSETS
            nextCoords = []
            for xOff, yOff in OFFSETS:
                tmpX, tmpY = x + xOff, y + yOff
                if inBound(tmpX, tmpY, grid)\
                    and grid[tmpY, tmpX] != '.'\
                    and (x, y) in getNextCoords(grid, tmpX, tmpY):
                    nextCoords.append((tmpX, tmpY))
            return nextCoords
        case '|': return [(x, y - 1), (x, y + 1)]
        case '-': return [(x + 1, y), (x - 1, y)]
        case 'L': return [(x, y - 1), (x + 1, y)]
        case 'J': return [(x, y - 1), (x - 1, y)]
        case '7': return [(x, y + 1), (x - 1, y)]
        case 'F': return [(x, y + 1), (x + 1, y)]
        case '.': return []

# === Part One ===
def partOne(grid):
    stack = deque()
    start = findStart(grid)

    # Keep track of visited pipes. Only update if the new distance is
    # _less_ than the previous distance.
    global visited
    visited = {}

    global OFFSETS
    for xOff, yOff in OFFSETS:
        x, y = start[0] + xOff, start[1] + yOff
        if inBound(x, y, grid) and grid[y, x] != '.' and start in getNextCoords(grid, x, y):
            stack.append((x, y, 1))
    visited[start] = 0

    while stack:
        x, y, dist = stack.pop()
        visited[(x, y)] = dist

        for coord in getNextCoords(grid, x, y):
            if coord in visited and visited[coord] <= dist:
                continue

            stack.append((coord[0], coord[1], dist + 1))

    return max(visited.values())

# === Part Two ===
def getLoop(grid: np.ndarray) -> Generator[tuple[int, int], None, None]:
    startCoord = findStart(grid)
    currCoord = startCoord

    visited = set()
    visited.add(currCoord)

    yield currCoord

    while True:
        nextCoords = getNextCoords(grid, *currCoord)
        nextCoords = [coord for coord in nextCoords if coord not in visited]

        if not nextCoords:
            break

        for coord in nextCoords:
            visited.add(coord)
            currCoord = coord
            yield coord

            if currCoord == startCoord: return
            break # Literally just to force one path at the start.

def partTwo(grid):
    loop = shapely.Polygon(list(getLoop(grid)))
    shapely.prepare(loop)

    minX, minY, maxX, maxY = loop.bounds
    points = [
        (x, y) for x, y in np.ndindex(grid.shape)
        if minX <= x <= maxX and minY <= y <= maxY
    ]

    return sum(loop.contains(shapely.Point(x, y)) for y, x in points)

def partTwoNoCheats(grid):
    cellsInside = 0
    loop = set(getLoop(grid))
    for y, x in np.ndindex(grid.shape):
        if (x, y) not in loop:
            grid[y, x] = '.'
    lines = [''.join(line) for line in grid]

    for y, line in enumerate(lines):
        boundsSeen = 0
        for x, char in enumerate(line):
            match char:
                case '.': cellsInside += boundsSeen % 2 != 0
                case '|' | 'J' | 'L': boundsSeen += 1

    return cellsInside

# === Run ===
if __name__ == "__main__":
    grid = parseGrid()

    timeAvgAndPrint("Part One", 100, partOne, grid)
    timeAvgAndPrint("Part Two", 100, partTwo, grid)
    timeAvgAndPrint("Part Two", 100, partTwoNoCheats, grid)
