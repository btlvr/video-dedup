import os, subprocess
import datetime
import cv2
import uuid
from pathlib import Path
from logger import prettify_path
import functools

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

# decorator for caching methods/properties of objects
class memoized(object):
	def __init__(self, func):
		self.func = func
		self.cache = {}

	def __call__(self, *args):
		try:
			if args in self.cache:
				return self.cache[args]
			else:
				value = self.func(*args)
				self.cache[args] = value
				return value
		except TypeError:
			return self.func(*args)

	def __repr__(self):
		return self.func.__repr__()

	def __get__(self, obj, objtype):
		return functools.partial(self.__call__, obj)

class File(object):
	def __init__(self, path):
		self.path = Path(path).expanduser().resolve()
	
	@property
	@memoized
	def stat(self):
		return self.path.stat()

	@property
	@memoized
	def size(self):
		return self.stat.st_size
	
	@property
	def extension(self):
		if '.' in self.path.name:
			return self.path.name.split('.')[-1]
		else:
			return None

	def is_video(self):
		return self.extension in movie_extensions

	@property
	@memoized
	def pretty_path(self):
		return prettify_path(self.path)

	def __str__(self):
		return str(self.path)

	def __eq__(self, other):
		return self.path == other.path.absolute()

	def __hash__(self):
		return hash(self.path)

	def __repr__(self):
		class_name = self.__class__.__name__
		return f'{class_name}({self.path.name})'

class Video(File):
	def __init__(self, path):
		super().__init__(path)
		self.broken = False

	# get duration of vidoe with ffprobe
	@memoized
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
		#TODO: set as broken if ffprobe command complains to STDERR?
		return duration

	def is_video(self):
		return self.extension in movie_extensions

	# capture an opencv image of the video at specified timestamp
	def frame_at(self, seconds):
		#TODO: avoid temporary path, make ffmpeg output image directly to STDOUT and read with cv2
		#TODO: allow for negative timestamp values (from end)
		#TODO: let user specify times in arguments as HH:MM:SS

		# convert to HH:MM:SS format for ffmpeg (needed?)
		timestamp = str(datetime.timedelta(0,seconds))

		# temporary path for image
		image_path = f'/tmp/.frame_{uuid.uuid4()}.bmp' # bmp used to avoid wasting time compressing

		# build and invoke ffpmeg command
		#TODO: is -noaccurate_seek helping?
		cmd = [
			'ffmpeg', '-y',
			'-noaccurate_seek',
			'-ss', timestamp,
			'-i', self.path,
			'-vframes', '1',
			'-q:v', '2',
			image_path
		]
		subprocess.call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
		
		# load the temporary image with cv2 and remove
		frame = cv2.imread(image_path)
		os.remove(image_path)
		return frame

	def hash_at(self, seconds):
		return cv2.img_hash.blockMeanHash(self.frame_at(seconds))