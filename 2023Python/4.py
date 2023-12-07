import re
from functools import cache

from template import getLines, timeAvgAndPrint

PATTERN = r":(.*)\|(.*)"

def strToSet(input):
	return frozenset(map(int, filter(None, input.strip().split(' '))))

def parseInput():
	lines = getLines(4)
	cards = filter(None, [next(iter(re.findall(PATTERN, line)), None) for line in lines])
	return[(strToSet(card[0]), strToSet(card[1])) for card in cards]

@cache
def numWinning(card):
	return len(set(card[0]).intersection(set(card[1])))

# === PART ONE ===
def partOne(cards):
	totalPoints = 0
	
	for card in cards:
		wins = numWinning(card)
		if wins <= 0:
			continue
		totalPoints += 2 ** (wins - 1)
	
	return totalPoints

# === PART TWO ===		

def partTwo(cards):
	consider = [1] * len(cards)
	
	for ind, card in enumerate(cards):
		numExtra = numWinning(card)
		for i in range(numExtra):
			consider[i + ind + 1] += consider[ind]
	
	return sum(consider)

# === RUN ===
if __name__ == "__main__":
	cards = parseInput()

	timeAvgAndPrint("Part One", 100, partOne, cards)
	timeAvgAndPrint("Part Two", 100, partTwo, cards)
	