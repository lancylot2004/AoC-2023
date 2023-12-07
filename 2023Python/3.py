import numpy as np
import re
from scipy.signal import convolve2d

from template import getLines, timeAvgAndPrint

KERNEL = np.array([
	[1, 1, 1],
	[1, 0, 1],
	[1, 1, 1]
])
PATTERN = r"\d+"
NON_SYMBOLS = np.array(list("0123456789."))

# === Part One ===
def loadSchem():
	return np.array([list(line.strip()) for line in getLines(3)])

def partOne(lines):
	sumParts = 0
	symbolMap = ~np.isin(lines, NON_SYMBOLS) 
	adjSymbolMap = convolve2d(symbolMap, KERNEL, mode='same', boundary='fill', fillvalue=0)
	
	for y, row in enumerate(lines):
		for match in re.finditer(PATTERN, ''.join(row)):
			start, end = match.start(), match.end()
			
			if np.any(adjSymbolMap[y, start:end] > 0):
				sumParts += int(match.group())
	
	return sumParts
	
# === Part Two ===
def partTwo(schem):
	numbers = []
	
	for y, row in enumerate(schem):
		row_numbers = [
			(match.start(), match.end() - match.start(), int(match.group()))
			for match in re.finditer(r"\d+", ''.join(row))
		]
		numbers.append(row_numbers)
		
	gears = {}
						
	# Iterate over numbers and find adjacent '*' symbols
	for row, numbers in enumerate(numbers):
		for startX, length, value in numbers:
			# Given a position, find adjacent '*'s and log them.
			rangeY = (max(-1, -row), min(2, len(schem) - row))
			rangeX = (max(-1, -startX), min(length + 1, len(schem[0]) - startX))
			for i, j in [
				(i, j) for i in range(*rangeY) for j in range(*rangeX)]:
				if schem[row + i][startX + j] == '*':
					key = (row + i, startX + j)
					gears.setdefault(key, []).append(value)
					
			
	return sum([val[0] * val[1] for key, val in gears.items() if len(val) == 2])

# === Run ===
if __name__ == "__main__":
	schem = loadSchem()

	timeAvgAndPrint("Part One", 100, partOne, schem)
	timeAvgAndPrint("Part Two", 100, partTwo, schem)
