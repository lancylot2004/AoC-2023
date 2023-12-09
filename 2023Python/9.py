from functools import reduce

from template import getLines, timeAvgAndPrint

def parseSeqs():
    lines = getLines(9)
    seqs = [[int(item) for item in line.strip().split(' ')] for line in lines]
    return seqs

def predictNext(seq):
    currSeq = seq
    result = 0

    while not all([item == 0 for item in currSeq]):
        result += currSeq[-1]
        currSeq = [j - i for i, j in zip(currSeq, currSeq[1:])]
    
    return result

def predictPrev(seq):
    currSeq = seq
    diffs = [seq[0]]

    while not all([item == 0 for item in currSeq]):
        currSeq = [j - i for i, j in zip(currSeq, currSeq[1:])]
        diffs.append(currSeq[0])
    
    return reduce(lambda x, y: y - x, reversed(diffs))

# === Part One ===
def partOne(seqs):
    return sum(predictNext(seq) for seq in seqs)

# === Part Two ===
def partTwo(seqs):
    return sum(predictPrev(seq) for seq in seqs)

# === Run ===
if __name__ == "__main__":
    seqs = parseSeqs()

    timeAvgAndPrint("Part One", 100, partOne, seqs)
    timeAvgAndPrint("Part Two", 100, partTwo, seqs)
