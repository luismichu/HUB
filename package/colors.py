import os
os.system('<nul set /p = \033[0m')

def red(text):
	return ('\x1b[31m' + str(text) + '\033[0m')

def green(text):
	return ('\x1b[32m' + str(text) + '\033[0m')

def yellow(text):
	return ('\x1b[33m' + str(text) + '\033[0m')

def blue(text):
	return ('\x1b[34m' + str(text) + '\033[0m')