#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ## #############################################################
# tcboard.py
#
# Author: Mauricio Matamoros
# Licence: MIT
# Date:
#
# ## #############################################################

import re
import sys
import time
from os import path, _exit
from threading import Thread
from tkinter import *

from PIL import Image, ImageTk, ImageEnhance

from .led import LED
from .sevenseg import SevenSeg
from .bcd7seg import BCD7Seg

class TempCtrlBoard:
	def __init__(self):

		# GUI
		self.gui = Tk(className=' Temperature Control Board')
		self._io_pins = {}
		for i in range(1, 28):
			self._io_pins[i] = None
		self._initialize_components()
		self.running = True
	# end def

	def __del__(self):
		_exit(1)
	# end def

	def _initialize_components(self):
		# set window size
		self.gui.geometry("510x270")
		#set window color
		self.gui.configure(bg='#296e01')
		self.gui.protocol("WM_DELETE_WINDOW", self._on_closing)
		# Create canvas
		self.canvas = Canvas(self.gui, width=510, height=270, bg='#296e01', bd=0, highlightthickness=0, relief='ridge')
		self.canvas.pack()
		self._draw_canvas()
		self.canvas.after(1, self._redraw)
	# end def

	def _draw_canvas(self):
		self.canvas.delete(ALL)
		# Add 7-segments to canvas
		# self.sevenSeg.draw(self.canvas, 197, 90)
		# Add LEDs to canvas
		# xpos = 20
		# ypos = 20
		# for led in self.leds:
		# 	led.draw(self.canvas, xpos, ypos)
		# 	xpos += 60
		self.canvas.update()
	# end def

	def _redraw(self):
		self._update_status()
		self._draw_canvas()
		if self.running:
			self.canvas.after(20, self._redraw)
	# end def

	def _on_closing(self):
		self.running = False
		self.gui.destroy()
	# end def

	def _update_status(self):
		pass
	# end def


	def connect(self, cable):
		pass
	# end def

