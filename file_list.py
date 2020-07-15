from video import Video
from args import args
import os
from pathlib import Path
import pathlib

for func in [Path, Path.expanduser, Path.resolve]:
	args.dirs = map(func, args.dirs)

for path in args.dirs:
	if not path.exists():
		print(f'supplied path {path} does not exist')
		exit(1)


args.dirs = list(args.dirs)
print(args.dirs)

exit()

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