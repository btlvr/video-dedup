from video import Video
from args import args
import os
from pathlib import Path
import pathlib

for func in [Path, Path.expanduser, Path.resolve]:
	args.dirs = list(map(func, args.dirs))

for path in args.dirs:
	if not path.exists():
		print(f'supplied path {path} does not exist')
		exit(1)

all_files = set()
for path in args.dirs:
	if path.is_dir():
		all_files = all_files.union(set(path.iterdir()))
	else:
		all_files.add(path)

videos = list(filter(Video.is_video, map(Video, all_files)))