from math import prod, sqrt, floor, ceil

from template import getLines, timeAvgAndPrint
        
def numWaysAboveCurr(totTime, currBest):
    phi = totTime / 2
    psi = sqrt(((totTime ** 2) / 4) - currBest)
    
    upper = phi + psi
    lower = phi - psi
    
    upper = upper - 1 if upper.is_integer() else floor(upper)
    lower = lower + 1 if lower.is_integer() else ceil(lower)
    return upper - lower + 1
    
# === Part One ===
def partOne(timeLine, distLine):
    times = [int(time) for time in timeLine[5:].strip().split(' ') if time != '']
    dists = [int(dist) for dist in distLine[9:].strip().split(' ') if dist != '']
    
    return prod(ways for ways in map(lambda args: numWaysAboveCurr(*args), zip(times, dists)))

# === Part Two ===
def partTwo(timeLine, distLine):
    time = int(timeLine[5:].strip().replace(' ', ''))
    dist = int(distLine[9:].strip().replace(' ', ''))
    
    return numWaysAboveCurr(time, dist)

if __name__ == "__main__":
    lines = getLines(6)
    timeLine, distLine = next(lines), next(lines)

    timeAvgAndPrint("Part One", 100, partOne, timeLine, distLine)
    timeAvgAndPrint("Part Two", 100, partTwo, timeLine, distLine)
    