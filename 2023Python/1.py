import regex as re

from template import getLines, timeAvgAndPrint

MATCH = {
	'one': 1,
	'two': 2,
	'three': 3,
	'four': 4,
	'five': 5,
	'six': 6,
	'seven': 7,
	'eight': 8,
	'nine':  9
}

INT_PATTERN = r"\d"
PATTERN = r"(one|two|three|four|five|six|seven|eight|nine|[0-9])"
	
# === Part One ===
def partOne(lines):
	total = 0
	
	for line in lines:
		digits = re.findall(INT_PATTERN, line)
		num = int(digits[0]) * 10 + int(digits[-1])
		total += num
	
	return total

# === Part Two ===
def partTwo(lines):
	total = 0
	
	for line in lines:
		digits = [
			int(item) if len(item) == 1 else MATCH[item]
			for item in re.findall(PATTERN, line, overlapped=True)
		]
		num = int(digits[0]) * 10 + int(digits[-1])
		total += num
	
	return total

# === Run ===
if __name__ == "__main__":
	lines = list(getLines(1))

	timeAvgAndPrint("Part One", 100, partOne, lines)
	timeAvgAndPrint("Part Two", 100, partTwo, lines)
	