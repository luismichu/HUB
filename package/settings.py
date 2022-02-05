from xml.dom import minidom
from xml.parsers.expat import ExpatError

class Settings:
	parse_exception = ExpatError

	def __init__(self, default = False, path = None):
		if path is not None:
			settins_path = path
		elif default == True:
			settins_path = 'settings/default_settings.xml'
		else:
			settins_path = 'settings/settings.xml'

		self.settings = minidom.parse(settins_path).documentElement

	def get_settings_dict(self):
		childNodes = [child for child in self.settings.childNodes if type(child) == minidom.Element]
		self.settings_dict = {child.tagName:child.firstChild.data for child in childNodes}

		return self.settings_dict