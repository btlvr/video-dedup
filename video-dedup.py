#! python3

from functools import *
import sys, os, subprocess
import time, datetime
import cv2, numpy
import random, uuid
from tqdm import tqdm
import argparse
from video import Video

parser = argparse.ArgumentParser(description='Find and remove duplicate videos')

parser.add_argument(
	'--no-color',
	dest='no_color',
	action='store_const',
	const=True, default=False,
	help='Disable color output'
)

parser.add_argument(
	"--duration-threshold",
	type=int,
	default=1,
	help="How different the durations of two videos must be in order to be considered unique"
)

parser.add_argument(
	'dirs',
	nargs='+',
	help='Directories'
)

parser.add_argument(
	"--hash-threshold",
	type=int,
	default=10,
	help="How different two frame hashes must be in order to be considred unique"
)

parser.add_argument(
	'-H',
	'--hashes',
	nargs='+',
	type=int,
	default=[1],
	help='list of timestamps (in seconds) to compare frame hashes at',
)

parser.add_argument(
	'-e',
	'--exclude',
	nargs='+',
	type=str,
	default=[],
	help='list of strings to exclude Videos',
)



args = parser.parse_args()

# terminal colors
#######################################
color = {
	'default'     : "\033[39m",
	'black'       : "\033[30m",
	'red'         : "\033[31m",
	'green'       : "\033[32m",
	'yellow'      : "\033[33m",
	'blue'        : "\033[34m",
	'magenta'     : "\033[35m",
	'cyan'        : "\033[36m",
	'lgray'       : "\033[37m",
	'dgray'       : "\033[90m",
	'lred'        : "\033[91m",
	'lgreen'      : "\033[92m",
	'lyellow'     : "\033[93m",
	'lblue'       : "\033[94m",
	'lmagenta'    : "\033[95m",
	'lcyan'       : "\033[96m",
	'white'       : "\033[97m"
}

if args.no_color:
	for c in color:
		color[c] = ''





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
		
def list_Videos(dir):
	for dirpath, subdirs, Videos in os.walk(dir):
		for Video in Videos:
			yield dirpath+'/'+Video

videos = []
for folder in args.dirs:
	videos += [Video(f) for f in list_Videos(folder) if Video(f).is_video()]

videos_clean = []
for video in videos:
	include = True
	for exclude in args.exclude:
		if exclude.lower() in video.path.lower():
			include = False
	if include:
		videos_clean += [video]

videos = videos_clean

pools = DuplicatePools(videos)

last_num_vids = None

def removal_status():
	new_len = len(pools)
	print(f'    {color["yellow"]}{new_len}{color["green"]} videos remaining{color["default"]}\n')

print(f'{color["blue"]}found {color["green"]}{len(pools)}{color["blue"]} videos{color["default"]}\n')

if args.duration_threshold:
	print(f'{color["magenta"]}excluding videos with durations that differ by more than {color["yellow"]}{args.duration_threshold}{color["magenta"]} seconds{color["default"]}')
	pools.expand(lambda v : v.duration(), lambda a, b : abs(a-b) <= args.duration_threshold)
	removal_status()
else:
	print(f'{color["yellow"]}It\'s probably a good idea to use {color["green"]}--duration-threshold{color["yellow"]}.{color["default"]}\n')

for timestamp in args.hashes:
	print(f'{color["magenta"]}comparing hashes at {color["yellow"]}{timestamp}s{color["default"]}')
	pools.expand(lambda v : v.hash_at(timestamp), lambda a, b : abs(numpy.mean(a-b) <= args.hash_threshold))
	removal_status()

pools.print()











