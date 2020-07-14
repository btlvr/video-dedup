from functools import *
import os
import time
import numpy
from tqdm import tqdm
import argparse
from colors import color

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

	def expand(self, fingerprint, compare):
		fingerprints = {}
		for item in tqdm(reduce(set.union, self.pools)):
			try:
				fingerprints[item] = fingerprint(item)
			except:
				fingerprints[item] = None
		
		new = {}
		for pool in self.pools:
			for item_a in pool:
				for item_b in pool:
					if item_a == item_b:
						continue
					new[item_a] = new.get(item_a, set({item_a}))

					f_a, f_b = (fingerprints[item_a], fingerprints[item_b])
					if f_a is not None and f_b is not None:
						if compare(f_a, f_b):
							new[item_a].add(item_b)
							new[item_a].add(item_a)
			
		self.pools = [set({item}).union(new[item]) for item in new]
		
		self.clean()
		self.pools = self.pools[::-1]
		self.clean()

	def clean(self):
		for index_a, pool_a in enumerate(self.pools):
			for index_b, pool_b in enumerate(self.pools):
				if index_a < index_b:
					if pool_a.issubset(pool_b):
						self.pools[index_a] = set()

		self.pools = [pool for pool in self.pools if len(pool) > 1]

	def __len__(self):
		return len(reduce(set.union, self.pools))