from colors import colors as c
from pathlib import Path
from tqdm import tqdm

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

def path_does_not_exist(path):
	print(f'{c["red"]}error: supplied path {prettify_path(path)}{c["red"]} does not exist')

def progress_bar(item, text_color=c['dgray'], bar_color=c['dgray']):
	bar_format = "%s{l_bar}%s{bar}%s{r_bar}" 
	bar_format %= (text_color, bar_color, text_color)
	return tqdm(
		item,
		bar_format=bar_format
	)
	print(c["default"])

def prettify_path(path):
	path_colors = {
		'slash':                 c['dgray'],
		'extension_dot_color':   c['dgray'],
		'parent':                c['blue'],
		'extension_color':       c['blue']
	}
	
	components = []
	while path.absolute() != Path(path.anchor):
		components += [path.name]
		path = path.parent
	components = components[::-1]

	slash = path_colors['slash'] + '/' + path_colors['parent']
	
	name, ext = components[-1], None
	if '.' in components[-1]:
		name, ext = components[-1].split('.',-1)

	pretty_str  = slash
	pretty_str += slash.join(components[:-1]) 
	pretty_str += slash
	pretty_str += name
	if ext is not None:
		pretty_str += path_colors['extension_dot_color'] + '.'
		pretty_str += path_colors['extension_color'] + ext
	pretty_str += c["default"]

	return pretty_str








