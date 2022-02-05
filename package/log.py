from time import localtime, strftime

log_name = ''

def get_time():
	return strftime('%H:%M:%S', localtime())

def get_date():
	return strftime('%y%m%d%H%M%S', localtime())

def log(*text, priority = 'Log'):
	result = ' '
	if type(text[0]) is tuple:
		result = ' '.join(str(t) for t in text[0])
	else:
		result = ' '.join(str(t) for t in text)

	to_write = '[' + priority + '] ' + get_time() + ': ' + result
	print(to_write)
	with open(log_name, 'a') as log_file:
		log_file.write(to_write + '\n')

def warning(*text):
	log(text, priority = 'Warning')

def error(*text):
	log(text, priority = 'ERROR')