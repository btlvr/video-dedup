#! python3

from functools import *
import os
import time
import numpy
from tqdm import tqdm

from video import Video
from duplicate_pools import DuplicatePools
from colors import color, disable_color
from args import args


if args.no_color:
	disable_color()
	
def list_videos(dir):
	for dirpath, subdirs, Videos in os.walk(dir):
		for Video in Videos:
			yield dirpath+'/'+Video

videos = []
for folder in args.dirs:
	videos += [Video(f) for f in list_videos(folder) if Video(f).is_video()]

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