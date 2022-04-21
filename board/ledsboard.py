#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ## #############################################################
# ledsboard.py
#
# Author:  Mauricio Matamoros
# Licence: MIT
# Date:    2020.03.01
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
from .__common import _img, _get_sprites, _set_kill_handler

class LedsBoard:
	def __init__(self):

		# GUI
		self.gui = Tk(className='GPIO LED Board')
		self.sevenSeg = SevenSeg()
		self.leds = [ LED() for i in range(0, 8) ]
		self.BCD7Seg = BCD7Seg(self.sevenSeg)
		self.BCD7Seg.ena = 0
		self._io_pins = {}
		for i in range(1, 28):
			self._io_pins[i] = None
		self._initialize_components()
		_set_kill_handler(self.close)
		self.running = True
	# end def

	def __del__(self):
		_exit(1)

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
		self.sevenSeg.draw(self.canvas, 197, 90)
		# Add LEDs to canvas
		xpos = 20
		ypos = 20
		for led in self.leds:
			led.draw(self.canvas, xpos, ypos)
			xpos += 60
		self.canvas.update()
	# end def

	def _redraw(self):
		if not self.running:
			return
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
		led_pins = [15, 18, 23, 24, 25, 8, 7, 12]

		# 16, 20, 21, 26
		if self._io_pins[16] and self._io_pins[20] and self._io_pins[21] and self._io_pins[26]:
			bcd = 8*self._io_pins[26].read()
			bcd+= 4*self._io_pins[21].read()
			bcd+= 2*self._io_pins[20].read()
			bcd+= 1*self._io_pins[16].read()
			self.BCD7Seg.bcd = bcd
		else:
			self.BCD7Seg.bcd = 0
		for i in range(len(led_pins)):
			if self._io_pins[led_pins[i]] and self._io_pins[led_pins[i]].read():
				self.leds[i].on()
			else:
				self.leds[i].off()
	# end def

	def connect(self, cable):
		"""cable is an dictionary of 27 objects with read() and write()
		methods whose keys are the number of the pin, starting in 1"""
		for pin in self._io_pins:
			if not pin in cable:
				continue
			if not hasattr(cable[pin], 'read'):
				raise Exception('{} object has no read attribute', cable[pin])
			self._io_pins[pin] = cable[pin]
		# end for
	# end def

	def close(self, *args):
		print("Shutting down GUI")
		self._on_closing()


