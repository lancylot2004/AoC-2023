from copy import deepcopy
from os import path
from time import perf_counter_ns
from tqdm import tqdm
from typing import Any, Callable, Generator

def getLines(day: int) -> Generator[str, None, None]:
    """Gets the lines of the input file for the given day.

    Args:
        day (int): Day to get the input for.

    Yields:
        Generator[str, None, None]: Lines of the input file.
    """
    with open(path.join(path.dirname(__file__), "inputs", f"{day}.txt"), 'r') as file:
        for line in file:
            yield line
            
def timeAndPrint(name: str, fun: Callable[..., Any], *args: Any) -> None:
    """Calls `fun` and prints the time it took to run, along with its result.

    Args:
        name (str): Human-readable name of this function call.
        fun (Callable[..., Any]): Function to call.
    """

    start = perf_counter_ns()
    # No need to deepcopy args here since only one call is made.
    res = fun(*args)
    end = perf_counter_ns()
    print(f"{name} after {(end - start) / 1_000_000:.3f}ms: {res}")

def timeAvgAndPrint(name: str, repeats: int, fun: Callable[..., Any], *args: Any):
    """Calls `fun` `repeats` times, and prints the average time along with its result. Additionally
    asserts that all calls to `fun` return the same result.

    Args:
        name (str): Human-readable name of this function call.
        repeats (int): Number of times to call `fun`.
        fun (Callable[..., Any]): Function to call.
        *args (Any): Arguments to pass to `fun`.
    """

    assert repeats > 0

    times = []
    res = None
    for _ in tqdm(range(repeats), desc=name, leave=False):
        start = perf_counter_ns()
        # Deepcopy args since some of my functions modify them.
        tmpRes = fun(*deepcopy(args))

        if res is not None:
            assert tmpRes == res
        res = tmpRes

        end = perf_counter_ns()
        times.append(end - start)
    
    avgTime = sum(times) / len(times)
    print(f"{name} after avg. {avgTime / 1_000_000:.3f}ms: {res}")