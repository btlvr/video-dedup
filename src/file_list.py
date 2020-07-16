from video import Video
from args import args
from pathlib import Path
import logger
import sys, os

# take list of paths from STDIN if available
if not sys.stdin.isatty():
	args.dirs += [p for p in sys.stdin.read().split('\n') if len(p.strip())]

# make all paths absolute
for func in [Path, Path.expanduser, Path.resolve]:
	args.dirs = list(map(func, args.dirs))

# sanity check paths
for path in args.dirs:
	if not path.exists():
		logger.path_does_not_exist(path)
		exit(1)

# given an array of Paths, recursively yield all files in directories
def files_in(paths):
	for path in paths:
		if path.is_dir():
			yield from files_in(path.iterdir())
		else:
			yield path

# filter out all non-video files, and convert to Video class
videos = list(filter(Video.is_video, map(Video, set(files_in(args.dirs)))))