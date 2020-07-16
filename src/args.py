import argparse

parser = argparse.ArgumentParser(description='Find and remove duplicate videos')

parser.add_argument(
	'--no-color',
	dest='no_color',
	action='store_const',
	const=True, default=False,
	help='Disable color output'
)

parser.add_argument(
	"--duration-threshold",
	type=int,
	default=1,
	help="How different the durations of two videos must be in order to be considered unique"
)

parser.add_argument(
	'dirs',
	nargs='*',
	help='Directories',
)

parser.add_argument(
	"--hash-threshold",
	type=int,
	default=10,
	help="How different two frame hashes must be in order to be considred unique"
)

parser.add_argument(
	'-H',
	'--hashes',
	nargs='+',
	type=int,
	default=[1],
	help='list of timestamps (in seconds) to compare frame hashes at',
)

parser.add_argument(
	'--list',
	dest='list_videos',
	action='store_const',
	const=True, default=False,
	help='print the videos which will be operated on and exit'
)

parser.add_argument(
	'--keep-prog',
	dest='keep_prog',
	action='store_const',
	const=True, default=False,
	help='don\'t clear progress bars when they reach 100%'
)

#parser.add_argument(
#	'-e',
#	'--exclude',
#	nargs='+',
#	type=str,
#	default=[],
#	help='list of strings to exclude Videos',
#)

args = parser.parse_args()