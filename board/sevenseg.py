#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ## #############################################################
# sevenseg.py
#
# Author: Mauricio Matamoros
# Licence: MIT
# Date:
#
# ## #############################################################

from tkinter import *
from PIL import Image, ImageTk, ImageEnhance

from .__common import _img, _get_sprites

class SevenSeg:
	def __init__(self):
		sprites = _get_sprites(_img("7s.png"), 116)
		self._bgi = ImageTk.PhotoImage(sprites[0])
		self._fgi = ImageTk.PhotoImage(sprites[1])
		self._sai = ImageTk.PhotoImage(sprites[2])
		self._sbi = ImageTk.PhotoImage(sprites[3])
		self._sci = ImageTk.PhotoImage(sprites[4])
		self._sdi = ImageTk.PhotoImage(sprites[5])
		self._sei = ImageTk.PhotoImage(sprites[6])
		self._sfi = ImageTk.PhotoImage(sprites[7])
		self._sgi = ImageTk.PhotoImage(sprites[8])
		self._dpi = ImageTk.PhotoImage(sprites[9])
		self.a = 0
		self.b = 0
		self.c = 0
		self.d = 0
		self.e = 0
		self.f = 0
		self.g = 0
		self.dp = 0
	# end def

	def draw(self, canvas, xpos, ypos):
		canvas.create_image(xpos, ypos, anchor=NW, image=self._bgi)
		if self.a:
			canvas.create_image(xpos, ypos, anchor=NW, image=self._sai)
		if self.b:
			canvas.create_image(xpos, ypos, anchor=NW, image=self._sbi)
		if self.c:
			canvas.create_image(xpos, ypos, anchor=NW, image=self._sci)
		if self.d:
			canvas.create_image(xpos, ypos, anchor=NW, image=self._sdi)
		if self.e:
			canvas.create_image(xpos, ypos, anchor=NW, image=self._sei)
		if self.f:
			canvas.create_image(xpos, ypos, anchor=NW, image=self._sfi)
		if self.g:
			canvas.create_image(xpos, ypos, anchor=NW, image=self._sgi)
		if self.dp:
			canvas.create_image(xpos, ypos, anchor=NW, image=self._dpi)
		canvas.create_image(xpos, ypos, anchor=NW, image=self._fgi)
	# end def
