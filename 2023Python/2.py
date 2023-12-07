from functools import reduce
import re

LINE_PATTERN = r"Game (\d{1,3}): (.*?)$"
BAG = {
	"red": 12,
	"green": 13,
	"blue": 14
}

# === Part One ===
def checkReveal(reveal):
	color, count = reveal
	
	return count <= BAG[color]

def parseGame(game):
	reveals = game.split(',')
	reveals = [reveal.strip().split(' ') for reveal in reveals]
	return {reveal[1]:int(reveal[0]) for reveal in reveals}

def checkGame(game):
	reveals = parseGame(game)
	
	return all([checkReveal(reveal) for reveal in reveals.items()])

def parseLine(line):
	id, rawGames = re.findall(LINE_PATTERN, line)[0]
	games = rawGames.strip().split(';')
	
	return id, games

def partOne(path):
	sumInd = 0
	
	with open(path, 'r') as file:
		for line in file:
			id, games = parseLine(line)
			
			if all([checkGame(game) for game in games]):
				sumInd += int(id)
	
	print(f"Part One: {sumInd}")
			
# === Part Two ===

def getLinePow(line):
	_, games = parseLine(line)
	result = {
		color: max((parseGame(game).get(color, 0) for game in games), default=0) 
		for color in ["red", "green", "blue"]
	}
	return reduce(lambda x, y: x * y, list(result.values()))
	
def partTwo(path):
	sumPow = 0
	
	with open(path, 'r') as file:
		for line in file:
			sumPow += getLinePow(line)

	print(f"Part Two: {sumPow}")
			
# === Run ===
if __name__ == "__main__":
	partOne("input.txt")
	partTwo("input.txt")