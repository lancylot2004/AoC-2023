from z3 import Real, Solver

from template import getLines, timeAvg

RANGE_MIN, RANGE_MAX = 2 * 10 ** 14, 4 * 10 ** 14

def getStones():
    stones = []
    for line in getLines(24):
        pos, vel = line.split('@')
        x, y, z = map(int, pos.split(','))
        vx, vy, vz = map(int, vel.split(','))
        stones.append((x, y, z, vx, vy, vz))
    
    return stones

@timeAvg("Part One", 100)
def partOne(stones):
    res = 0
    for curr, then in ((curr, then) for i, curr in enumerate(stones) for then in stones[i + 1:]):
        xa, xb, xc, xd = curr[0], curr[0] + curr[3], then[0], then[0] + then[3]
        ya, yb, yc, yd = curr[1], curr[1] + curr[4], then[1], then[1] + then[4]

        den = ((xa - xb) * (yc - yd) - (ya - yb) * (xc - xd))
        if den:
            detOfDiff = ((xa - xb) * (yc - yd) - (ya - yb) * (xc - xd))
            numerA, numerB = xa * yb - ya * xb, xc * yd - yc * xd
            intrX = (numerA * (xc - xd) - numerB * (xa - xb)) / detOfDiff
            intrY = (numerA * (yc - yd) - numerB * (ya - yb)) / detOfDiff

            valid = (intrX > xa) == (xb > xa) and (intrX > xc) == (xd > xc)
            if valid and RANGE_MIN <= intrX <= RANGE_MAX and RANGE_MIN <= intrY <= RANGE_MAX:
                res += 1
    
    return res

@timeAvg("Part Two", 100)
def partTwo(stones):
    X, Y, Z, VX, VY, VZ = map(Real, ['x', 'y', 'z', 'vx', 'vy', 'vz'])
    TS = [Real(f'T{i}') for i in range(len(stones))]

    solver = Solver()
    for ind, stone in enumerate(stones):
        solver.add(X + TS[ind] * VX - stone[0] - TS[ind] * stone[3] == 0)
        solver.add(Y + TS[ind] * VY - stone[1] - TS[ind] * stone[4] == 0)
        solver.add(Z + TS[ind] * VZ - stone[2] - TS[ind] * stone[5] == 0)
    _ = solver.check()
    model = solver.model()

    return model.eval(X + Y + Z)

if __name__ == "__main__":
    stones = getStones()

    # partOne(stones)
    partTwo(stones)
