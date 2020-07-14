from functools import *
from tqdm import tqdm
from colors import colors as color
from operator import *
from collections import defaultdict
from contextlib import suppress

# return all (a, b) pairs in i, such that criteria(a, b) == True
def pairings(i, criteria):
	permutations = [set((a, b) for a in i if criteria(a, b)) for b in i]
	return reduce(set.union, permutations)

class DuplicatePools(object):
	def __init__(self, items):
		self.pools = [set(items)]

	def print(self):
		hbar_width = 10
		for pool in self.pools:
			print(f'{color["dgray"]}{"-"*hbar_width}{color["default"]}')
			for item in pool:
				print(f'    {color["yellow"]}{item}{color["default"]}')
		print(f'{color["dgray"]}{"-"*hbar_width}{color["default"]}')

	def items(self):
		return reduce(set.union, self.pools)

	def fingerprint(self, func):
		fingerprints = defaultdict(lambda : None)
		for item in tqdm(self.items()):
			with suppress(Exception): fingerprints[item] = func(item)
		return fingerprints

	def expand(self, fingerprint, compare):
		fingerprints = self.fingerprint(fingerprint)
		new = {}
		for pool in self.pools:			
			for item_a, item_b in pairings(pool, ne):
				new[item_a] = new.get(item_a, set({item_a}))
				f_a, f_b = fingerprints[item_a], fingerprints[item_b]
				if f_a is None or f_b is None:
					continue
				if compare(f_a, f_b):
					new[item_a].add(item_b)
					new[item_a].add(item_a)
		self.pools = list(map(set, new.values()))
		self.clean()

	def clean(self):
		# delete subpools
		for a, b in pairings((range(len(self.pools))), ne):			
			if self.pools[a].issubset(self.pools[b]):
				self.pools[a] = set()

		# remove empty or single-item pools
		self.pools = [p for p in self.pools if len(p) > 1]
	
	def __len__(self):
		return len(self.items())