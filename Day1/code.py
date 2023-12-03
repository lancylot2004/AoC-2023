#!/usr/bin/env python3

import regex as re

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

PATTERN = r"(one|two|three|four|five|six|seven|eight|nine|[0-9])"

with open('input.txt', 'r') as file:
	total = 0
	for line in file:
			
		digits = [
			int(item) if len(item) == 1 else MATCH[item]
			for item in re.findall(PATTERN, line, overlapped=True)
		]
		num = int(digits[0]) * 10 + int(digits[-1])
		print(num)
		total += num
	print(total)
