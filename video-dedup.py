#! python3

from functools import *
import os
import time
import numpy

from video import Video
from duplicate_pools import DuplicatePools
import logger
from args import args

def list_files(dir):
	for dirpath, subdirs, Videos in os.walk(dir):
		for Video in Videos:
			yield dirpath+'/'+Video

videos = set()
for folder in args.dirs:
	videos = videos.union(set(map(Video, list_files(folder))))

def file_is_excluded(file):
	if not file.is_video:
		return True
	return False

videos = [v for v in videos if not file_is_excluded(v)]

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