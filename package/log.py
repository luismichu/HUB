from time import localtime, strftime
from package import colors

def get_time():
	return strftime('%H:%M:%S', localtime())

def get_date():
	return strftime('%y%m%d%H%M%S', localtime())

log_name = 'default_log_' + get_date() + '.txt'
log_level = 0

def log(*text, priority = 'Log', color = None, level = 0):
	if log_level <= int(level):
		result = ' '
		if type(text[0]) is tuple:
			result = ' '.join(str(t) for t in text[0])
		else:
			result = ' '.join(str(t) for t in text)

		to_write = '[' + priority + '] ' + get_time() + ': ' + result
		if color is not None:
			to_print = '[' + color(priority) + '] ' + get_time() + ': ' + result
		else:
			to_print = to_write
		print(to_print)
		with open(log_name, 'a') as log_file:
			log_file.write(to_write + '\n')

def warning(*text):
	log(text, priority = 'Warning', color = colors.yellow, level = 1)

def error(*text):
	log(text, priority = 'ERROR', color = colors.red, level = 2)