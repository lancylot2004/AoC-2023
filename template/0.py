from template import getLines, timeAvgAndPrint

# ...

def partOne(someArs, someMoreArgs):
    pass

def partTwo(maybeSomeOtherArgs):
    pass

if __name__ == "__main__":
    someArgs, someMoreArgs = getLines(0)
    maybeSomeOtherArgs = [arg for arg in someArgs if arg in someMoreArgs]
    timeAvgAndPrint("Part 1", 100, partOne, someArgs, someMoreArgs)
    timeAvgAndPrint("Part 2", 100, partTwo, maybeSomeOtherArgs)