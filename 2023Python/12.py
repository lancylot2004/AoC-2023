from dataclasses import dataclass
from functools import cache
from typing import List

from template import getLines, timeAvgAndPrint

@dataclass
class Cond:
    pattern: str
    numbers: List[int]

    @cache
    @staticmethod
    def recurse(restPattern, restNums, restLen):
        # Base Case
        if len(restNums) == 0:
            return 1 if all(char in ".?" for char in restPattern) else 0

        nextGroup = restNums[0]
        restNums = restNums[1:]
        after = sum(restNums) + len(restNums)

        count = 0
        for pad in range(restLen - nextGroup - after + 1):
            perm = '.' * pad + '#' * nextGroup + '.'
            if all(a == b or a =='?' for a, b in zip(restPattern, perm)):
                nextPattern = restPattern[pad + nextGroup + 1:]
                count += Cond.recurse(nextPattern, restNums, restLen - nextGroup - pad - 1)

        return count
    
    @property
    def possiblePatterns(self):
        return Cond.recurse(self.pattern, tuple(self.numbers), len(self.pattern))

def parseConds():
    lines = [line.strip().split() for line in getLines(12)]
    return [Cond(line[0], [int(x) for x in line[1].split(',')]) for line in lines]

def partOne(conds):
    return sum(cond.possiblePatterns for cond in conds)

def partTwo(conds):
    conds = [Cond('?'.join([cond.pattern] * 5), cond.numbers * 5) for cond in conds]
    return partOne(conds)

# === Run ===
if __name__ == "__main__":
    conds = parseConds()

    timeAvgAndPrint("Part One", 100, partOne, conds)
    timeAvgAndPrint("Part Two", 100, partTwo, conds)
