import os, subprocess
import datetime
import cv2
import uuid
from pathlib import Path
from logger import prettify_path

movie_extensions = [
	'mp4',
	'wmv',
	'm4a',
	'flv',
	'mov',
	'm4v',
	'mkv',
	'webm',
	'mpg'
]

class Video(object):
	def __init__(self, path):
		self.path = Path(path).expanduser().resolve()
		self.broken = False
		self.size = None

	def duration(self):
		cmd = [
			'ffprobe',
			'-v',
			'error',
			'-show_entries',
			'format=duration',
			'-of',
			'default=noprint_wrappers=1:nokey=1',
			str(self.path)
		]
		try:
			duration = float(subprocess.check_output(cmd, stderr=subprocess.DEVNULL))
		except subprocess.CalledProcessError:
			self.broken = True
			return None

		return duration

	def size(self):
		if self.size is None:
			self.size = 5

	def extension(self):
		return self.path.name.split('.')[-1]

	def is_video(self):
		return self.extension() in movie_extensions

	def frame_at(self, seconds):
		timestamp = str(datetime.timedelta(0,seconds))
		image_path = f'/tmp/.frame_{uuid.uuid4()}.png'
		cmd = 'ffmpeg', '-y', '-ss', timestamp, '-i', self.path, '-vframes', '1', '-q:v', '2', image_path
		subprocess.call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
		frame = cv2.imread(image_path)
		os.remove(image_path)
		return frame

	def hash_at(self, seconds):
		return cv2.img_hash.blockMeanHash(self.frame_at(seconds))

	def __str__(self):
		#return str(self.path)
		return prettify_path(self.path)

	def __eq__(self, other):
		return self.path == other.path.absolute()

	def __hash__(self):
		return hash(self.path)