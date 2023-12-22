from template import getLines, time

class Brick():
    def __init__(self, line: str) -> None:
        c0Raw, c1Raw = (half.split(',') for half in line.strip().split('~'))
        c0 = [int(x) for x in c0Raw]
        c1 = [int(x) for x in c1Raw]

        self.xRange, self.yRange = (c0[0], c1[0] + 1), (c0[1], c1[1] + 1)
        self.h0, self.h1 = c0[2], c1[2]
        self.supporting, self.restsOn = set(), []
        self.falling = False

    @property
    def minHeight(self) -> int:
        return min(self.h0, self.h1)

    @property
    def maxHeight(self) -> int:
        return max(self.h0, self.h1)
    
    def __and__(self, other: 'Brick') -> bool:
        """Bricks overlap?"""
        xOverlap = (self.xRange[0] < other.xRange[1]) and (self.xRange[1] > other.xRange[0])
        if not xOverlap:
            return False

        return (self.yRange[0] < other.yRange[1]) and (self.yRange[1] > other.yRange[0])

    def recursiveFall(self) -> int:
        self.falling = True
        count = 0
        for x in self.supporting:
            # All blocks underneath is falling?
            if len([y for y in x.restsOn if not y.falling]) == 0:
                count += 1 + x.recursiveFall()
        return count

def freefall(bricks: list[Brick]):
    for ind, brick in enumerate(bricks):
        for x in range(ind - 1, -1, -1):
            restHeight = brick.restsOn[0].maxHeight if brick.restsOn else 1

            # Check overlap in `xy`, ignore `z`.
            if brick & bricks[x]:
                newHeight = bricks[x].maxHeight
                if not brick.restsOn or newHeight > restHeight:
                    for y in brick.restsOn:
                        y.supporting.remove(brick)
                    brick.restsOn = [bricks[x]]
                    bricks[x].supporting.add(brick)
                elif newHeight == restHeight:
                    brick.restsOn.append(bricks[x])
                    bricks[x].supporting.add(brick)

        diff = brick.minHeight - (brick.restsOn[0].maxHeight + 1) if brick.restsOn else brick.minHeight - 1
        brick.h0 -= diff
        brick.h1 -= diff

def getBricks():
    bricks = [Brick(line) for line in getLines(22)]
    bricks = sorted(bricks, key = lambda x: x.minHeight)
    freefall(bricks)
    return bricks

@time("Part One")
def partOne(bricks):
    return sum(all([len(x.restsOn) > 1 for x in brick.supporting]) for brick in bricks)

@time("Part Two")
def partTwo(bricks):
    total = 0
    for brick in bricks:
        for x in bricks:
            x.falling = False

        total += brick.recursiveFall()

    return total

if __name__ == "__main__":
    bricks = getBricks()
    partOne(bricks)
    partTwo(bricks)
