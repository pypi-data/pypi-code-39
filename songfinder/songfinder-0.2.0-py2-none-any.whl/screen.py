# -*- coding: utf-8 -*-
from __future__ import division

import warnings
import sys
try:
	import tkinter as tk
except ImportError:
	import Tkinter as tk
import screeninfo

from songfinder import commandLine
from songfinder import exception
from songfinder import globalvar

class Screen(object):
	def __init__(self, width=720, height=480, xposition=0, yposition=0, stringScreen=None):
		if not stringScreen:
			try:
				self.width = width
				self.height = height
				self.xposition = xposition
				self.yposition = yposition
			except ValueError:
				warnings.warn("Erreur de lecture des donnees de l'ecran")
				self._defaultScreen()
		else:
			self._setScreen(stringScreen)

	def _setScreen(self, stringScreen):
		list_fois = stringScreen.split('x')
		if len(list_fois) != 2:
			warnings.warn('Erreur de lecture de la resolution de l''ecran, '
					'le format des donnees n''est pas valide : "%s". '
					'Le format valide est : "wxh+pw+ph'%stringScreen)
			self._defaultScreen()
		else:
			list_plus = list_fois[1].split('+')
			if len(list_plus) != 3:
				warnings.warn('Erreur de lecture de la position de l''ecran, '
										'le format des donnees n''est pas valide : "%s". '
										'Le format valide est : "wxh+pw+ph'%stringScreen)
				self._defaultScreen()
			else:
				try:
					self.width = float(list_fois[0])
					self.height = float(list_plus[0])
					self.xposition = float(list_plus[1])
					self.yposition = float(list_plus[2])
				except ValueError:
					warnings.warn("Erreur de lecture des donnees de l'ecran")
					self._defaultScreen()

	def _defaultScreen(self):
		self._width = 720
		self._height = 480
		self._xposition = 0
		self._yposition = 0

	@property
	def xposition(self):
		return self._xposition

	@xposition.setter
	def xposition(self, value):
		self._xposition = int(value)

	@property
	def yposition(self):
		return self._yposition

	@yposition.setter
	def yposition(self, value):
		self._yposition = int(value)

	@property
	def width(self):
		return self._width

	@width.setter
	def width(self, value):
		self._width = int(value)

	@property
	def height(self):
		return self._height

	@height.setter
	def height(self, value):
		self._height = int(value)

	@property
	def ratio(self):
		if self._height != 0:
			ratio = self._width/self._height
		else:
			ratio = 1
		return ratio

	def __str__(self):
		out = ''.join([str(self._width), 'x', str(self._height), '+', \
						str(self._xposition), '+', str(self._yposition)])
		return out

	def isWidgetInScreen(self, widget):
		xposition = widget.winfo_x() - self.xposition
		yposition = widget.winfo_y() - self.yposition
		if xposition  >= 0 \
			and xposition < self.width \
			and yposition >= 0 \
			and yposition < self.height:
				return True
		else:
			return False

	def centerFrame(self, frame):
		newx = (self.width-frame.winfo_reqwidth())//2
		newy = (self.height-frame.winfo_reqheight())//2
		frame.geometry('+%d+%d'%(newx, newy))

	def resizeFrame(self, frame, width, height):
		newWidth = min(self.width, width)
		newHeight = min(self.height, height)
		clipx = self.width-newWidth+self.xposition
		clipy = self.height-newHeight+self.yposition
		newx = max(min(frame.winfo_x(), clipx), self.xposition)
		newy = max(min(frame.winfo_y(), clipy), self.yposition)
		frame.geometry('%dx%d+%d+%d'%(newWidth, newHeight, newx, newy))

	def __repr__(self):
		return repr(str(self))

class Screens(object):
	def __init__(self):
		self._screens = []
		self._maxScreens = sys.maxsize

	def __getitem__(self, index):
		if len(self._screens) == 0:
			self.update()
		if index > len(self._screens):
			raise Exception('You asked for screen number %d but '
				'only %d screens are available.'%(index, len(self._screens)))
		return self._screens[index]

	def __len__(self):
		if len(self._screens) == 0:
			self.update()
		return len(self._screens)

	@property
	def maxScreens(self):
		return self._maxScreens

	@maxScreens.setter
	def maxScreens(self, value):
		if self._maxScreens != value:
			self._maxScreens = value
			self.update()

	def update(self, referenceWidget=None, verbose=True):
		del self._screens[:]
		try:
			monitors = screeninfo.get_monitors()
		except NotImplementedError:
			monitors = []
		if len(monitors) > 0:
			for monitor in monitors:
				if len(self._screens) == 0:
					ratio = 0.9
				else:
					ratio = 1
				self._add(Screen(monitor.width, monitor.height, \
							monitor.x, monitor.y), ratio=ratio)
		else:
			warnings.warn('Screeninfo did not output any screen infos')
			if globalvar.myOs == 'windows':
				self._getWindowsScreens()
			elif globalvar.myOs == 'ubuntu':
				self._getLinuxScreens()
			elif globalvar.myOs == 'darwin':
				self._getMacOsScreens()
			else:
				warnings.warn("No screen found, OS is not supported.")
				self._getLinuxScreens()

			if len(self._screens) > self._maxScreens:
				del self._screens[self._maxScreens:]
		if referenceWidget:
			self._reorder(referenceWidget)
		if verbose:
			print("Using %d screens: "%len(self._screens))
			for screenCouple in self._screens:
				print('	Full: %s, Usable: %s'\
					%(str(screenCouple[0]), str(screenCouple[1])))

	def _reorder(self, referenceWidget):
		for i,screen in enumerate(self._screens):
			if screen[0].isWidgetInScreen(referenceWidget):
				self._screens[0], self._screens[i] = self._screens[i], self._screens[0]
				break

	def _add(self, screen, usableScreen=None, ratio=1):
		if not usableScreen:
			usableWidth = screen.width*ratio
			usableHeight = screen.height*ratio
			usablex = 0
			usabley = 0
			usableScreen = Screen(width=usableWidth, \
						height=usableHeight, \
						xposition=usablex, \
						yposition=usabley)
		self._screens.append((screen, usableScreen))

	def _getLinuxScreens(self):
		if not self._getXrandrScreen():
			if not self._getByTopLevelScreens():
				self._getDefaultScreen()

	def _getWindowsScreens(self):
		if not _getWindowsTopLevelScreens():
			self._getDefaultScreen()

	def _getMacOsScreens(self):
		if not self_getXrandrScreen():
			if not self._getWindowServerScreens():
				if not self._getSystemProfilerScreens():
					if not self._getByTopLevelScreens():
						self._getDefaultScreen()

	def _getDefaultScreen(self):
		self._add(Screen(width=720, height=480), ratio=0.9)

	def _getXrandrScreen(self):
		xrandr = commandLine.MyCommand('xrandr')
		try:
			xrandr.checkCommand()
		except exception.CommandLineError:
			return False
		else:
			code, out, err = xrandr.run(['|', 'grep \\*', '|', "cut -d' ' -f4"])
			if code != 0:
				warnings.warn("Erreur de detection des ecrans\nError %s\n%s"%(str(code), err))
				return False
			liste_res = out.strip('\n').splitlines()
			if '' in liste_res:
				liste_res.remove('')
			if not liste_res:
				liste_res = []
				code, out, err = xrandr.run(['|', 'grep connected'])
				if code != 0:
					warnings.warn("Erreur de detection des ecrans\nError %s\n%s"%(str(code), err))
					return False
				line_res = out.replace('\n', '')
				deb = line_res.find('connected')
				fin = line_res.find('+', deb+1)
				deb = line_res.rfind(' ', 0, fin)
				liste_res.append(line_res[deb+1: fin])

			code, out, err = xrandr.run()
			if code != 0:
				warnings.warn("Erreur de detection des ecrans: Error %s"%str(code) + "\n" + err)
				return False
			deb = 0
			liste_respos = []
			for res in liste_res:
				deb = out.find(res + '+', deb)
				fin = out.find(' ', deb)
				if len(self._screens) == 0:
					ratio = 0.9
				else:
					ratio = 1
				self._add(Screen(stringScreen=out[deb:fin]), ratio=ratio)
				deb = fin + 1
		return True

	def _getWindowsTopLevelScreens(self):
		try:
			test = tk.Toplevel()
		except tk.TclError:
			return False
		else:
			test.wm_attributes('-alpha', 0)
			test.withdraw()
			test.update_idletasks()
			test.state('zoomed')
			test.withdraw()
			ww1 = test.winfo_width()
			hh1 = test.winfo_height()
			test.overrideredirect(1)
			test.state('zoomed')
			test.withdraw()
			w1 = test.winfo_width()
			h1 = test.winfo_height()
			posw1 = test.winfo_x()
			posh1 = test.winfo_y()
			test.state('normal')
			test.withdraw()
			self._add(Screen(w1, h1, posw1, posh1), \
					usableScreen=Screen(width=ww1, height=hh1, \
								xposition=posw1, yposition=posh1))
			# Scan for second screen
			test.overrideredirect(1)
			for decal in [[w, h] for w in [w1, w1//2, -w1//8] for h in [h1//2, h1, -h1//8]]:
				test.geometry("%dx%d+%d+%d"%(w1//8, h1//8, decal[0], decal[1]))
				test.update_idletasks()
				test.state('zoomed')
				test.withdraw()
				if test.winfo_x() != posw1 or test.winfo_y() != posh1:
					newW = test.winfo_width()
					newH = test.winfo_height()
					newPosW = test.winfo_x()
					newPosH = test.winfo_y()
					self._add(Screen(width=newW, height=newH, \
								xposition=newPosW, yposition=newPosH))
				test.state('normal')
				test.withdraw()
			test.destroy()
			return True

	def _getWindowServerScreens(self):
		read = commandLine.MyCommand('defaults read')
		try:
			read.checkCommand()
		except exception.CommandLineError:
			return False
		code, out, err = xrandr.run(['/Library/Preferences/com.apple.windowserver.plist'])
		if code != 0:
			warnings.warn("Erreur de detection des ecrans\nError %s\n%s"%(str(code), err))
			return False
		return False

	def _getSystemProfilerScreens(self):
		systemProfiler = commandLine.MyCommand('system_profiler')
		try:
			systemProfiler.checkCommand()
		except exception.CommandLineError:
			return False
		keyWord = 'Resolution:'
		code, out, err = xrandr.run(['SPDisplaysDataType', '|', 'grep', keyWord])
		if code != 0:
			warnings.warn("Erreur de detection des ecrans\nError %s\n%s"%(str(code), err))
			return False
		widthOffset = 0
		heightOffset = 0
		for line in out.split('\n'):
			if len(self._screens) == 0:
				ratio = 0.9
			else:
				ratio = 1
			deb = line.find(keyWord) + len(keyWord)
			end = line.find('+', deb)
			width = line[deb:end].strip(' ')
			height = line[end+1:].strip(' ')
			self._add(Screen(width=width, height=height, \
							xposition=widthOffset, yposition=heightOffset), \
							ratio=ratio)
			widthOffset = width
		return False

	def _getByTopLevelScreens(self):
		try:
			test = tk.Toplevel()
		except tk.TclError:
			return False
		else:
			test.wm_attributes('-alpha', 0)
			test.withdraw()
			test.update_idletasks()

			posw1 = test.winfo_x()
			posh1 = test.winfo_y()
			scrW = test.winfo_screenwidth()
			scrH = test.winfo_screenheight()
			test.destroy()
			if scrW > 31*scrH//9:
				scrW = scrW//2
			elif scrW < 5*scrH//4:
				scrH = scrH//2
			self._add(Screen(width=scrW, height=scrH), ratio=0.9)
			return True

def get_new_size(image, width, height):
	im_w, im_h = image.size
	aspect_ratio = im_w/im_h
	new_im_w = min(width, height*aspect_ratio)
	new_im_h = new_im_w//aspect_ratio
	return int(new_im_w), int(new_im_h)

def choose_orient(screen, ratio, decal_w, decal_h):
	use_w = screen.width-decal_w
	use_h = screen.height-decal_h
	use_ratio = use_w/use_h
	if use_ratio < ratio:
		return tk.TOP
	else:
		return tk.LEFT

def getRatio(ratio, default=None):
	try:
		a, b = ratio.split('/')
		value = round(int(a)/int(b), 3)
	except (ValueError, AttributeError):
		if default:
			value = default
		else:
			value = 16/9
	return value
