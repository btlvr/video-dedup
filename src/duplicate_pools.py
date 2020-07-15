import logger
from colors import colors as color
from operator import *
from functools import *
from contextlib import suppress
from collections import defaultdict
from multiprocessing import Pool

from pathos.multiprocessing import ProcessingPool

# return all (a, b) pairs in i, such that criteria(a, b) == True
def pairings(i, criteria):
	permutations = [set((a, b) for a in i if criteria(a, b)) for b in i]
	return reduce(set.union, permutations)

class DuplicatePools(object):
	def __init__(self, items):
		self.pools = [set(items)]

	def print(self):
		for pool in self.pools:
			logger.hbar()
			for item in pool:
				print('    ', item.pretty_path)
		logger.hbar()

	def items(self):
		if not len(self.pools):
			return {}
		elif not len(self.pools[0]):
			return {}
		return reduce(set.union, self.pools)

	def fingerprint_multi(self, func):
		def func_safe(item):
			#with suppress(Exception):
			return func(item)
			return None
		items = list(self.items())

		#results = ProcessingPool().map(func_safe, items)
		results = list(map(func_safe, items))

		return dict(zip(items, results))
	
	'''
	def fingerprint(self, func):
		fingerprints = defaultdict(lambda : None)
		for item in logger.progress_bar(self.items()):
			with suppress(Exception): fingerprints[item] = func(item)
		return fingerprints
	'''

	def check_if_done(self):
		if len(self) == 1:
			print("no duplicates found")
			exit(0)
		if len(self) == 0:
			print("no duplicates found")
			exit(0)

	def expand(self, fingerprint, compare):
		self.check_if_done()
		fingerprints = self.fingerprint_multi(fingerprint)

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
		self.check_if_done()

	def clean(self):
		# delete subpools
		for a, b in pairings((range(len(self.pools))), ne):
			if self.pools[a].issubset(self.pools[b]):
				self.pools[a] = set()

		# remove empty or single-item pools
		self.pools = [p for p in self.pools if len(p) > 1]
	
	def __len__(self):
		return len(self.items())