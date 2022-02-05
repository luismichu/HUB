from pystray import MenuItem as MenuItemStray
import pystray
from PIL import Image
import threading
import os

# Used in IconStray class, and executes a function when clicked
# Can have submenus
class SuperMenuItem(MenuItemStray):
	global position
	position = {}

	def __init__(self, name, ident, my_submenu = None, pos = None, function = None, state = False, radio = False):
		global position
		self.name = name
		self.ident = ident
		position.update({ident:0})
		if my_submenu == None:
			self.function = self.set_state
			self.my_function = function
		else:
			self.function = pystray.Menu(*list(my_submenu))
		self.my_state = state
		self.my_radio = radio
		self.pos = pos

		super().__init__(self.name, self.function, checked = self.get_state(), radio = self.my_radio)

	def set_state(self):
		global position
		position[self.ident] = self.pos
		self.my_state = True
		self.my_function()

	def get_state(self):
		def inner(item):
			return position[self.ident] == self.pos
		return inner
		

# Used in IconStray class, and executes a function when clicked
class MenuItem(SuperMenuItem):
	def __init__(self, name, function):
		self.name = name
		self.function = function

		super().__init__(self.name, -1,function = self.function, state = False, radio = False)

# Uses a tuple of MenuItems and runs in a different thread from main if necessary
class IconStray:
	def __init__(self, menu, title = 'default'):
		self.menu = menu + (pystray.Menu.SEPARATOR, MenuItem('Exit', self.icon_stop))
		self.title = title
		icon_name = 'package/data/icon2.png'
		if not os.path.exists(icon_name): raise FileNotFoundError('[EXCEPTION] The icon file is missing in ' + os.getcwd() + icon_name)
		self.image = Image.open(icon_name)
		self.icon = pystray.Icon(self.title, self.image, self.title, self.menu)

	def icon_stop(self):
		self.icon.stop()

	def run_no_threaded(self):
		self.icon.run()

	def run(self):
		icon_thread = threading.Thread(target = self.icon.run, args = ())
		icon_thread.start()

	def notify(self, notification_text = 'Default notification'):
		self.icon.notify(notification_text)
