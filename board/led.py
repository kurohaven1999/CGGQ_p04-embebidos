#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ## #############################################################
# led.py
#
# Author: Mauricio Matamoros
# Licence: MIT
# Date:
#
# ## #############################################################

from tkinter import *
from PIL import Image, ImageTk, ImageEnhance

from .__common import _img, _get_sprites

class LED:
	def __init__(self):
		sprites = _get_sprites(_img("ledr.png"), 50)
		self._on = False
		self._bg = ImageTk.PhotoImage(sprites[0])
		self._fg = ImageTk.PhotoImage(sprites[1])
		self._im = ImageTk.PhotoImage(sprites[2])
	# end def


	def on(self):
		self._on = True
	# end def

	def off(self):
		self._on = False
	# end def

	def draw(self, canvas, xpos, ypos):
		canvas.create_image(xpos, ypos, anchor=NW, image=self._bg)
		if self._on:
			canvas.create_image(xpos, ypos, anchor=NW, image=self._im)
		canvas.create_image(xpos, ypos, anchor=NW, image=self._fg)
	# end def
#end class
