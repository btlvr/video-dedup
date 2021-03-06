#! python3

import signal
def stop(signal, frame):
	exit(0)

signal.signal(signal.SIGINT, stop)

import os
import time
import numpy

from duplicate_pools import DuplicatePools
import logger
from args import args
from file_list import videos

if args.list_videos:
	logger.print_videos(videos)

pools = DuplicatePools(videos)

logger.found_n_videos(len(pools))

if args.duration_threshold:
	logger.excluding_by_duration(args.duration_threshold)
	pools.expand(
		lambda v : v.duration(),
		lambda a, b : abs(a-b) <= args.duration_threshold
	)
	logger.n_videos_remaining(len(pools))
else:
	logger.warn_duration_threshold()

for timestamp in args.hashes:
	logger.comparing_hashes_at(timestamp)
	pools.expand(
		lambda v : v.hash_at(timestamp),
		lambda a, b : abs(numpy.mean(a-b) <= args.hash_threshold)
	)
	logger.n_videos_remaining(len(pools))

pools.print()