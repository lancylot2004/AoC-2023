# AoC-2023

Advent of Code solutions for 2023, in Python (3.11). Code is usually not very good - I'm going for 
speed (points), not Employee of the Month :)

## Requirements

Alas, I know I am very lazy, so I like to take shortcuts and not write extra code wherever I can. 
Hence, some of my solutions require extra(non-inbuilt) packages:

- **Day 1**: `regex` for overlapping matches.
- **Day 3**: `scipy` for `convolve2d`, and `numpy` for general maths.
- **Day 5**: `intervaltree` for fast interval lookups.
- **Day 10**: `numpy` for general maths, and (**optional**) `shapely` for polygons.
- **Day 11**: `numpy` for general maths.

## Common Issues

Given the speedy nature of the code, here are a few common edge cases which ignore. 

- Trailing newlines in input - I always delete them manually.
- Some things can't be pickled by `deepcopy` in the template - usually generators. Just convert them to lists.

## Template

At some point along the way I decided that manually writing boilerplate code for each day was a waste of time, so I wrote `template.py`. It's hacky, and consists of `getLines`, `timeAndPrint` and `timeAvgAndPrint`. 

The folder structure it requires is as follows:
```
__init__.py
template.py
inputs/
	1.txt
	2.txt
	...
1.py
2.py
...
```

Then, in each day's file (e.g., `1.py`), add the following:
```Python
from template import getLines, timeAvgAndPrint

# ...

if __name__ == "__main__":
    someArgs, someMoreArgs = getLines(0)
    timeAvgAndPrint("Part 1", 100, partOne, someArgs, someMoreArgs)
    timeAvgAndPrint("Part 2", 100, partTwo, someArgs)
```

The template, although minimal, is resistant against
- Your functions modifying inputs.
- Literally nothing else - it's a very hacky template.

## Solution Outlines

I'm not sure why you've read so far - but since you have, here are some outlines and rationales for my solutions, in case you're interested / need a hint.

| Day | Notes |
| :-: | :---- |
| 1   | Regex is your friend. Especially in Part 2, overlapping matches is essentially cheating. :) |
| 2   |       |
| 3   | This one was tricky. `convolve2d` can help you with Part 1 (use Regex to then get the numbers), since you only had to consider at least one adjacency. But for Part 2, even though the logic is similar, the strict requirement of exactly **2** numbers meant that I had to keep a dictionary of all the gears. |
| 4   | Remember that Python `set`s have an `intersection` method.
| 5   | This one was also tricky. Part 1 could literally be hacked together with lists of numbers, but Part 2 required a more efficient solution. I chose `IntervalTree`s to simplify the numerous numbers to smaller ranges, and implemented custom methods for partial intersection and difference, since the original library does not consider these cases. |
| 6   | Technically does not even require code to solve - do some maths before you dig in! |
| 7   | Categorsation and comparison of hands was the key here. I chose to make a custom `@dataclass`, but there must be more efficient ways. |
| 8   | Part 1 could be hacked together with a simple while loop, but Part 2 required some more efficiency. I chose to store length of each cycle (time taken to get to a `\w{2}Z` node), and find their `lcm` - again, try maths! |
| 9   | Part one is the tail of the first sequence plus all the subsequent tails of the differences, and part two is the tail of the first minus all subsequent tails. |
| 10  | Another "curve-ball in part 2". It turns out you can just count the number of "border-crossings" a point has to the left (or right), and if it is odd, that means it is inside of the shape. In fact, since the question guarentees a valid loop, you only have to look for any one of `|JL`. Or, if you're feeling particularly lazy, use `shapely`! |