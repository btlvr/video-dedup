from video import Video
from args import args
from pathlib import Path
import logger
import sys, os

if not sys.stdin.isatty():
	args.dirs += [p for p in sys.stdin.read().split('\n') if len(p.strip())]

for func in [Path, Path.expanduser, Path.resolve]:
	args.dirs = list(map(func, args.dirs))

for path in args.dirs:
	if not path.exists():
		logger.path_does_not_exist(path)
		exit(1)

all_files = set()
for path in args.dirs:
	if path.is_dir():
		all_files = all_files.union(set(path.iterdir()))
	else:
		all_files.add(path)

#print(all_files)

videos = list(filter(Video.is_video, map(Video, all_files)))