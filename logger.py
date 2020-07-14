from colors import colors as c

def plural(num, name):
	if num == 1:
		return name
	else:
		return name+'s'

def found_n_videos(n):
	print(
		f'{c["blue"]}found ' +
		f'{c["green"]}{n}' +
		f'{c["blue"]} videos' +
		f'{c["default"]}\n'
	)

def n_videos_remaining(n):
	print(
		f'{c["green"]}{n}' +
		f'{c["blue"]} videos remaining' +
		f'{c["default"]}\n'
	)

def excluding_by_duration(n):
	print(
		f'{c["magenta"]}' +
		f'excluding videos with durations that differ by more than ' +
		f'{c["yellow"]}{n}' +
		f'{c["magenta"]} {plural(n, "second")}' +
		f'{c["default"]}'
	)

def warn_no_duration_threshold():
	print(
		f'{c["yellow"]}It\'s probably a good idea to use ' +
		f'{c["green"]}--duration-threshold' +
		f'{c["yellow"]}.{c["default"]}\n'
	)

def comparing_hashes_at(n):
	print(
		f'{c["magenta"]}comparing hashes at ' +
		f'{c["yellow"]}{n}' +
		f'{c["magenta"]}s' +
		f'{c["default"]}'
	)

def hbar(n=10):
	print(f'{c["dgray"]}{"-"*n}{c["default"]}')

def print_path(path):
	print(f'    {c["yellow"]}{path}{c["default"]}')