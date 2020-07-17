import logger
from colors import colors as color
from operator import *
from functools import *
from contextlib import suppress
from collections import defaultdict
from pool_map import pool_map

# yield all (a, b) pairs in i, such that criteria(a, b) == True
def pairings(i, criteria):
	for a in i:
		for b in i:
			if criteria(a, b):
				yield (a, b)

# class to represent sets of files that are potential duplicates
# these sets can be broken down into subsets as files are confirmed
# to be unique
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
		return reduce(set.union, self.pools) #TODO: convert to generator


	def fingerprint(self, func):
		# make a more mild-mannered version of func, which returns None if a
		# a problem occurs
		def func_safe(item):
			with suppress(Exception):
				return func(item)
			return None
		
		# map func onto the items currently in the pools, and return a dict,
		# for retrieval of the fingerprint values
		items = list(self.items())
		results = pool_map(func_safe, items, parallel=True, desc="calculating")
		return dict(zip(items, list(results)))
		

	def check_if_done(self):
		if len(self) <= 1:
			print("no duplicates found")
			exit(0)

	def expand(self, fingerprint, compare):
		# make sure there are still files left
		self.check_if_done()

		# compute fingerprints of each file for comparison
		fingerprints = self.fingerprint(fingerprint)
		
		# store comparison results in a dict, in which the keys are files,
		# and values are files that are potential duplicates of that file
		#TODO: give better name
		new = {}

		# compute number of total comparisons to be made (for progress bar)
		total_comparisons = sum([len(p)**2 - len(p) for p in self.pools])//2
		
		# make progress bar (manually updated in loop)
		pbar = logger.progress_bar(None, total=total_comparisons, desc="comparing")

		# iterate through every subpool of potential duplicates
		for pool in self.pools:

			# get all non-redundant (a, b) pairs from subpool where a != b 
			pool = list(pool)
			for index_a, index_b in pairings(range(len(pool)), lt):
				item_a, item_b = pool[index_a], pool[index_b]

				# avoid KeyError
				#TODO: switch to defaultdict
				new[item_a] = new.get(item_a, set({item_a}))

				# get fingerprints of items in pair currently being compared.
				# if either fingerprint is None, an error probably occured when
				# computing the fingerprint, so we can't consider this to be
				# evidence that the file is a duplicate
				f_a, f_b = fingerprints[item_a], fingerprints[item_b]
				if f_a is None or f_b is None:
					continue

				# if compare() indicates that these files are potential duplicates,
				# store that result in new
				if compare(f_a, f_b):
					new[item_a].add(item_b)
					new[item_a].add(item_a)

				# update progress bar, once per comparison
				#TODO: do such frequent updates impact performance?
				pbar.update(1)

		# obliterate tqdm
		pbar.close()
		
		# convert dict of new results into proper format (list of sets)
		self.pools = list(map(set, new.values()))
		
		# purge files that are no longer of interest and check to see if
		# there's still work to be done
		self.clean()
		self.check_if_done()

	def clean(self):
		# merge subpools
		for a, b in pairings((range(len(self.pools))), ne):
			if self.pools[a].issubset(self.pools[b]):
				self.pools[a] = set()

		# remove empty or single-item pools
		self.pools = [p for p in self.pools if len(p) > 1]
	
	# count number of files currently in the pools
	def __len__(self):
		return len(self.items())