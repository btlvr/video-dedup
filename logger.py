from colors import color, disable_color
from args import args
if args.no_color:
	disable_color()

def plural(num, name):
	if num == 1:
		return name
	else:
		return name+'s'

def found_n_videos(n):
	print(
		f'{color["blue"]}found ' +
		f'{color["green"]}{n}' +
		f'{color["blue"]} videos' +
		f'{color["default"]}\n'
	)

def excluding_by_duration(n):
	print(
		f'{color["magenta"]}' +
		f'excluding videos with durations that differ by more than ' +
		f'{color["yellow"]}{n}' +
		f'{color["magenta"]} {plural(n, "second")}' +
		f'{color["default"]}'
	)

def warn_no_duration_threshold():
	print(
		f'{color["yellow"]}It\'s probably a good idea to use ' +
		f'{color["green"]}--duration-threshold' +
		f'{color["yellow"]}.{color["default"]}\n'
	)

def comparing_hashes_at(n):
	print(
		f'{color["magenta"]}comparing hashes at ' +
		f'{color["yellow"]}{n}' +
		f'{color["magenta"]}s' +
		f'{color["default"]}'
	)