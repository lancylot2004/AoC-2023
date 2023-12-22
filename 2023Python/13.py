from template import getFile, timeAvgAndPrint

parsePatterns = lambda: [p.splitlines() for p in getFile(13).split("\n\n")]
lineDiff = lambda pattern, ind: sum(
    sum(a != b for a, b in zip(line[ind:], line[ind - 1::-1])) 
    for line in pattern
)
mirrorWithError = lambda pattern, error: sum(
    ind for ind in range(1, len(pattern[0])) if lineDiff(pattern, ind) == error
)

def part(patterns, error):
    total = 0
    for pattern in patterns:
        total += mirrorWithError(pattern, error)
        total += 100 * mirrorWithError([*zip(*pattern)], error)
    
    return total

if __name__ == "__main__":
    patterns = parsePatterns()

    timeAvgAndPrint("Part 1", 100, part, patterns, 0)
    timeAvgAndPrint("Part 2", 100, part, patterns, 1)