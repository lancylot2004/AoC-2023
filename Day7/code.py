#!/usr/bin/env python3

from collections import Counter
from dataclasses import dataclass
from enum import Enum

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

Type = Enum('Type', [
	"HIGH_CARD",
	"ONE_PAIR",
	"TWO_PAIR",
	"THREE_OF_A_KIND",
	"FULL_HOUSE",
	"FOUR_OF_A_KIND",
	"FIVE_OF_A_KIND"
])	

CARDS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T' ,'J', 'Q', 'K', 'A']
PART_TWO_FLAG = False

@dataclass
class Card:
	cards: str

	@property
	def counts(self) -> Counter:
		counts = Counter(self.cards)
		if not PART_TWO_FLAG:
			return counts
		
		if 'J' in counts:
			best_card = max((card for card in counts if card != 'J'), key=lambda x: (counts[x], CARDS.index(x)), default='2')
			counts[best_card] += counts['J']
			del counts['J']
		return counts
	
	@property
	def type(self) -> Type:
		if len(self.cards) != 5:
			raise ValueError("AoC has screwed me over or something...")
		
		match len(set(self.counts.keys())):
			case 5: return Type.HIGH_CARD
			case 4: return Type.ONE_PAIR
			case 3: return Type.THREE_OF_A_KIND if any(count == 3 for count in self.counts.values()) else Type.TWO_PAIR
			case 2: return Type.FOUR_OF_A_KIND if any(count == 4 for count in self.counts.values()) else Type.FULL_HOUSE
			case 1: return Type.FIVE_OF_A_KIND
	
	def __lt__(self, other):
		if self.type != other.type:
			return self.type.value < other.type.value
		
		for _, pairNum in enumerate(zip(self.cards, other.cards)):
			if pairNum[0] != pairNum[1]:
				return CARDS.index(pairNum[0]) < CARDS.index(pairNum[1])
		
		raise ValueError("AoC has screwed me over or something...")

def parseInput():
	cardsAndBids = [line.strip().split(' ') for line in getLines()]
	return [(Card(pair[0]), int(pair[1])) for pair in cardsAndBids]
		
# === Part One ===
def partOne(cardsAndBids):
	return sum([(ind + 1) * cardAndBid[1] for ind, cardAndBid in enumerate(sorted(cardsAndBids, key = lambda x: x[0]))])

if __name__ == "__main__":
	cardsAndBids = parseInput()
	timeAvgAndPrint("Part One", 100, partOne, cardsAndBids)
	PART_TWO_FLAG = True
	CARDS = ['J', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A']
	timeAvgAndPrint("Part Two", 100, partOne, cardsAndBids)