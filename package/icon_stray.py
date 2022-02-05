from pystray import MenuItem as MenuItemStray
import pystray
from PIL import Image
import threading
import os

# Can have submenus
class SuperMenuItem(MenuItemStray):
	def __init__(self, name, my_submenu = None, function = None, state = True, radio = False):
		self.name = name
		if my_submenu == None:
			self.function = function
		else:
			self.function = pystray.Menu(*list(my_submenu))
		self.state = state
		self.my_radio = radio

		super().__init__(self.name, self.function, checked = lambda item: self.state, radio = self.my_radio)

	def set_state(self, state = True):
		self.state = state
		print(super().submenu)
		for item in super().submenu().items():
			item.state = False
		print(self.state)

# Used in IconStray class, and executes a function when clicked
class MenuItem(SuperMenuItem):
	def __init__(self, name, function, state = False):
		self.name = name
		self.state = state
		self.function = function

		super().__init__(self.name, function = self.on_clicked, state = self.state, radio = True)

	def on_clicked(self):
		#icon.notify('Hello World!')
		#self.state = self.function()
		super().set_state(False)

# Uses a tuple of MenuItems and runs in a different thread from main
class IconStray:
	def __init__(self, menu, title = 'default'):
		self.menu = menu + (pystray.Menu.SEPARATOR, MenuItem('Exit', self.icon_stop))
		self.title = title
		icon_name = 'package/data/icon2.png'
		if not os.path.exists(icon_name): raise FileNotFoundError('[EXCEPTION] The file icon.png is missing in ' + os.getcwd())
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
