from itertools import combinations
import numpy as np

from template import getLines, timeAvgAndPrint

def parseImage():
    return np.array([[char for char in line.strip()] for line in getLines(11)])

def emptyBetween(i, j, knownEmpty):
    return len([k for k in knownEmpty if i < k < j])

def precomputeDists(dim, knownEmpty, expFact):
    distances = np.zeros((dim, dim), dtype=int)
    for i in range(dim):
        for j in range(i+1, dim):
            distances[i, j] = distances[j, i] = abs(i - j) + emptyBetween(i, j, knownEmpty) * (expFact - 1)
    return distances

def sumPairDists(image, expFact):
    positions = np.argwhere(image == "#")
    emptyRows = np.where(np.all(image == '.', axis=1))[0]
    emptyCols = np.where(np.all(image == '.', axis=0))[0]

    rowDistances = precomputeDists(image.shape[0], emptyRows, expFact)
    colDistances = precomputeDists(image.shape[1], emptyCols, expFact)

    totalDist = 0
    for gxy1, gxy2 in combinations(positions, 2):
        totalDist += rowDistances[gxy1[0], gxy2[0]] + colDistances[gxy1[1], gxy2[1]]

    return totalDist

# === Part One ===
def partOne(image):
    return sumPairDists(image, 2)

# === Part Two ===
def partTwo(image):
    return sumPairDists(image, 1_000_000)

# === Run ===
if __name__ == "__main__":
    image = parseImage()
    timeAvgAndPrint("Part One", 100, partOne, image)
    timeAvgAndPrint("Part Two", 100, partTwo, image)