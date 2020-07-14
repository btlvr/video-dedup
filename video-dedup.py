#! python3

from functools import *
import os
import time
import numpy

from video import Video
from duplicate_pools import DuplicatePools
import logger
from args import args

	
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

if args.duration_threshold:
	logger.excluding_by_duration(args.duration_threshold)
	pools.expand(lambda v : v.duration(), lambda a, b : abs(a-b) <= args.duration_threshold)
	logger.found_n_videos(len(pools))

else:
	logger.warn_duration_threshold()

for timestamp in args.hashes:
	logger.comparing_hashes_at(timestamp)
	pools.expand(lambda v : v.hash_at(timestamp), lambda a, b : abs(numpy.mean(a-b) <= args.hash_threshold))
	logger.n_videos_remaining(len(pools))

pools.print()