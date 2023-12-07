# AoC-2023

Advent of Code solutions for 2023, in Python.

- Code is usually not very good - I'm going for speed (points), not Employee of the Month :)
- Lots of repos delete their own `input.txt` before pushing - I respect that, but have kept mine so you can try out the code without having to fetch input files.

At some point along the way, I finally wrote a template - for loading files, calculating time taken and the such. If that's what you came for, here it is!

```Python
from time import perf_counter_ns

def getLines(path = "input.txt"):
	with open(path, 'r') as file:
		for line in file:
			yield line

def timeAndPrint(name, fun, *args):
	start = perf_counter_ns()
	res = fun(*args)
	end = perf_counter_ns()
	print(f"{name} after {(end - start) / 1_000_000:.3f}ms: {res}")

def timeAvgAndPrint(name, repeats, fun, *args):
	times = []
	res = None
	for _ in range(repeats):
		start = perf_counter_ns()
		res = fun(*args)
		end = perf_counter_ns()
		times.append(end - start)

	avgTime = sum(times) / len(times)
	print(f"{name} after avg. {avgTime / 1_000_000:.3f}ms: {res}")
```