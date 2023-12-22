from template import getLines, timeAvg, time

DIRS = [1, -1, 1j, -1j]
TARGET = 26501365

def cacheLines():
    return list(getLines(21))

def computeAttribs():
    grid = set()

    for row, line in enumerate(getLines(21)):
        for ind, char in enumerate(line):
            match char:
                case '#': grid.add(ind + row * 1j)
                case 'S': start = ind + row * 1j
    
    # grid, reach, gridWidth
    return grid, {0: set([start])}, ind + 1

@timeAvg("Part One", 100)
def partOne(grid, reach):
    while len(reach) <= 64:
        steps = max(reach.keys())
        reach[steps + 1] = set()

        for pos in reach[steps]:
            for dir in DIRS:
                if pos + dir not in grid:
                    reach[steps + 1].add(pos + dir)

    return len(reach[64])

@time("Part Two")
def partTwo(grid, reach, gridWidth):
    points = []

    while len(points) < 3:
        steps = max(reach.keys())

        if steps - 1 in reach:
            del reach[steps - 1]

        reach[steps + 1] = set()

        for pos in reach[steps]:
            for dir in DIRS:
                newPoint = pos + dir
                newX, newY = newPoint.real % gridWidth, newPoint.imag % gridWidth
                if newX + newY * 1j not in grid:
                    reach[steps + 1].add(pos + dir)

        if (steps - (gridWidth // 2) + 1) % gridWidth == 0:
            points.append(len(reach[max(reach.keys())]))

    c = points[0]
    b = points[1] - points[0]
    a = points[2] - points[1]
    x = TARGET // gridWidth

    return c + b * x + (x * (x - 1) // 2) * (a - b)

if __name__ == "__main__":
    grid, reach, gridWidth = computeAttribs()

    # timeAvgAndPrint("Part One", 100, partOne, grid, reach)
    partOne(grid, reach)
    partTwo(grid, reach, gridWidth)
