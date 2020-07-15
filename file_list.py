from video import Video
from args import args
import os
from pathlib import Path

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