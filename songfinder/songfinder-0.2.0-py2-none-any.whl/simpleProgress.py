# -*- coding: utf-8 -*-
from __future__ import division

try:
	import tkinter as tk
except ImportError:
	import Tkinter as tk
import ttk

from songfinder import guiHelper

class SimpleProgress(object):
	def __init__(self, title, mode='determinate', screens=None, **kwargs):
		self._fen = tk.Toplevel()
		self._fen.withdraw()
		self._fen.title('Progression')
		self._fen.resizable(False,False)
		self._mode = mode
		if screens:
			screens[0][1].centerFrame(self._fen)

		self.prog = tk.Label(self._fen, text=title, justify='left')
		self.prog_bar = ttk.Progressbar(self._fen, orient="horizontal",
											length=200, mode=self._mode, \
											value=0.0)
		self.cancel = tk.Button(self._fen, text='Annuler', command=self._cancel)
		self.prog.pack(side=tk.TOP)
		self.prog_bar.pack(side=tk.TOP)
		self.cancel.pack(side=tk.TOP)
		self._counter = 0

	def start(self, total=100, steps=100):
		self._fen.deiconify()
		guiHelper.upFront(self._fen)
		self._total = total
		self._ratio = (total+steps-1)//steps
		self.prog_bar["value"] = 0.0
		self.prog_bar["maximum"] = self._total
		self.prog_bar.start()

	def update(self):
		if self._mode == 'determinate':
			self._counter += 1
			self.prog_bar["value"] = self._counter
		if self._counter%self._ratio==0: # Lowers the graphical overhead
			self._fen.update()
			guiHelper.upFront(self._fen)

	def stop(self):
		self.prog_bar.stop()
		self._fen.destroy()

	def _cancel(self):
		self.stop()
