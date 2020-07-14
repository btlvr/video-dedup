#! python3

from functools import *
import os
import time
import numpy

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

def plural(num, name):
	if num == 1:
		return name
	else:
		return name+'s'

def removal_status():
	new_len = len(pools)
	print(
		' '*4 +
		f'{color["yellow"]}{new_len}' +
		f'{color["green"]} {plural(new_len, "video")}' +
		f' remaining{color["default"]}\n'
	)

print(
	f'{color["blue"]}found ' +
	f'{color["green"]}{len(pools)}' +
	f'{color["blue"]} videos' +
	f'{color["default"]}\n'
)

if args.duration_threshold:
	print(
		f'{color["magenta"]}' +
		f'excluding videos with durations that differ by more than ' +
		f'{color["yellow"]}{args.duration_threshold}' +
		f'{color["magenta"]} {plural(args.duration_threshold, "second")}' +
		f'{color["default"]}'
	)

	pools.expand(lambda v : v.duration(), lambda a, b : abs(a-b) <= args.duration_threshold)
	removal_status()
else:
	print(
		f'{color["yellow"]}It\'s probably a good idea to use ' +
		f'{color["green"]}--duration-threshold' +
		f'{color["yellow"]}.{color["default"]}\n'
	)

for timestamp in args.hashes:
	print(
		f'{color["magenta"]}comparing hashes at ' +
		f'{color["yellow"]}{timestamp}' +
		f'{color["magenta"]}s' +
		f'{color["default"]}')
	pools.expand(lambda v : v.hash_at(timestamp), lambda a, b : abs(numpy.mean(a-b) <= args.hash_threshold))
	removal_status()

pools.print()