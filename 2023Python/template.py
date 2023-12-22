from copy import deepcopy
from functools import wraps
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

def getFile(day: int) -> str:
    """Gets the contents of the input file for the given day.

    Args:
        day (int): Day to get the input for.

    Returns:
        str: Contents of the input file.
    """
    with open(path.join(path.dirname(__file__), "inputs", f"{day}.txt"), 'r') as file:
        return file.read()
    
def time(name: str) -> Callable[..., Any]:
    """Decorator that times a function's execution and prints the time alongw its result.

    Args:
        method (Callable[..., T]): Function to be timed and evaluated.

    Returns:
        Callable[..., T]: Decorated function.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        """Decorator function to time the provided function.

        Args:
            func (Callable[..., Any]): Function to time.

        Returns:
            Callable[..., Any]: Decorated function to time and print its execution.
        """

        @wraps(func)
        def wrapper(*args: Any) -> Any:
            """Wrapped function to time and print its execution.

            Args:
                *args (Any): Arguments to pass to the function.

            Returns:
                Any: Result of the function call.
            """

            start = perf_counter_ns()
            res = func(*args)
            end = perf_counter_ns()
            print(f"{name} after {(end - start) / 1_000_000:.3f}ms: {res}")
            return res

        return wrapper

    return decorator

def timeAvg(name: str, repeats: int) -> Callable[..., Any]:
    """Decorator that times a function's execution and prints the average time along with its result.

    Args:
        name (str): Human-readable name of the function call.
        repeats (int): Number of times to call the function.

    Returns:
        Callable[..., Any]: Decorated function to time and print its execution.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        """Decorator function to time the provided function.

        Args:
            func (Callable[..., Any]): Function to time.

        Returns:
            Callable[..., Any]: Decorated function to time and print its execution.
        """

        @wraps(func)
        def wrapper(*args: Any) -> Any:
            """Wrapped function to time and print its execution.

            Args:
                *args (Any): Arguments to pass to the function.

            Returns:
                Any: Result of the function call.
            """
            assert repeats > 0

            times = []
            res = None
            for _ in tqdm(range(repeats), desc = name, leave = False):
                start = perf_counter_ns()
                # Deepcopy args since some functions might modify them.
                tmpRes = func(*deepcopy(args))
                end = perf_counter_ns()
                times.append(end - start)

                if res is not None:
                    assert tmpRes == res
                res = tmpRes

            avgTime = sum(times) / len(times)
            print(f"{name} after avg. {avgTime / 1_000_000:.3f}ms: {res}")
            return res

        return wrapper

    return decorator

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