# Requirements: regex

import regex as re
from time import perf_counter_ns

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

def parseDigits(path):
	with open(path, 'r') as file:
		return file.readlines()
	
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
	start = perf_counter_ns()
	lines = parseDigits("input.txt")
	print(f"Part One: {partOne(lines)}")
	print(f"Part Two: {partTwo(lines)}")
	end = perf_counter_ns()
	print(f"Took {(end - start) / 1_000:.3f}us")
	