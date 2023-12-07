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