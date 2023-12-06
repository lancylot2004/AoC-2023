#!/usr/bin/env python3

from math import prod, sqrt, floor, ceil

def getLines(path):
	with open(path, 'r') as file:
		lines = file.readlines()
		
		# time(s), dist(s)
		return lines[0], lines[1]
		
def numWaysAboveCurr(totTime, currBest):
	phi = totTime / 2
	psi = sqrt(((totTime ** 2) / 4) - currBest)
	
	upper = phi + psi
	lower = phi - psi
	
	upper = upper - 1 if upper.is_integer() else floor(upper)
	lower = lower + 1 if lower.is_integer() else ceil(lower)
	return upper - lower + 1
	
# === Part One ===
def partOne(path):
	timeLine, distLine = getLines(path)
	
	times = [int(time) for time in timeLine[5:].strip().split(' ') if time != '']
	dists = [int(dist) for dist in distLine[9:].strip().split(' ') if dist != '']
	
	return prod(ways for ways in map(lambda args: numWaysAboveCurr(*args), zip(times, dists)))

# === Part Two ===
def partTwo(path):
	timeLine, distLine = getLines(path)
	
	time = int(timeLine[5:].strip().replace(' ', ''))
	dist = int(distLine[9:].strip().replace(' ', ''))
	
	return numWaysAboveCurr(time, dist)

if __name__ == "__main__":
	import time
	
	start = time.perf_counter_ns()
	print(f"Part One: {partOne('input.txt')}")
	print(f"Part TwoL {partTwo('input.txt')}")
	end = time.perf_counter_ns()
	print(f"Took {(end - start) / 1_000:.3f}us")
	