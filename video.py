import os, subprocess
import datetime
import cv2
import uuid

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
		self.path = path

	def duration(self):
		cmd = [
			'ffprobe',
			'-v',
			'error',
			'-show_entries',
			'format=duration',
			'-of',
			'default=noprint_wrappers=1:nokey=1',
			self.path
		]
		try:
			duration = float(subprocess.check_output(cmd))
		except subprocess.CalledProcessError:
			print(f'couldn\'t get duration for {self.path}')
			return None

		return duration

	def extension(self):
		return self.path.split('/')[-1].split('.')[-1]

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
		return self.path

	def __eq__(self, other):
		return self.path == other.path

	def __hash__(self):
		return hash(self.path)