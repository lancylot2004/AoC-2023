# AoC-2023

Advent of Code solutions for 2023, in Python.

- Code is usually not very good - I'm going for speed (points), not Employee of the Month :)
- Lots of repos delete their own `input.txt` before pushing - I respect that, but have kept mine so you can try out the code without having to fetch input files.

## Common Issues

Given the speedy nature of the code, here are a few common edge cases which ignore. 

- Trailing newlines in input - I always delete them manually.

## Template

At some point along the way I decided that manually writing boilerplate code for each day was a 
waste of time, so I wrote `template.py`. It's hacky, and consists of `getLines`, `timeAndPrint` and
`timeAvgAndPrint`. 

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