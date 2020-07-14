from args import args

colors = {
	'default'     : "\033[39m",
	'black'       : "\033[30m",
	'red'         : "\033[31m",
	'green'       : "\033[32m",
	'yellow'      : "\033[33m",
	'blue'        : "\033[34m",
	'magenta'     : "\033[35m",
	'cyan'        : "\033[36m",
	'lgray'       : "\033[37m",
	'dgray'       : "\033[90m",
	'lred'        : "\033[91m",
	'lgreen'      : "\033[92m",
	'lyellow'     : "\033[93m",
	'lblue'       : "\033[94m",
	'lmagenta'    : "\033[95m",
	'lcyan'       : "\033[96m",
	'white'       : "\033[97m"
}

if args.no_color:
	colors = dict.fromkeys(colors, '')