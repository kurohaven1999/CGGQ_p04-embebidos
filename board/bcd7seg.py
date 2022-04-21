#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ## #############################################################
# bcd7seg.py
#
# Author: Mauricio Matamoros
# Licence: MIT
# Date:
#
# ## #############################################################

from tkinter import *
from PIL import Image, ImageTk, ImageEnhance

class BCD7Seg:
	def __init__(self, sevenSeg):
		self.sevenSeg = sevenSeg
		self._ena = 1
		self._bcd = 0
		self._rom = {
			#    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, a, b, c, d, e, f
			0 : [1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1], # a
			1 : [1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0], # b
			2 : [1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0], # c
			3 : [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0], # d
			4 : [1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1], # e
			5 : [1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1], # f
			6 : [0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1], # g
		}
	# end def

	@property
	def bcd(self):
		return self._bcd
	# end def

	@bcd.setter
	def bcd(self, value):
		if value < 0:
			value = 0
		if value > 15:
			value = 15
		self._bcd = value
		self.sevenSeg.a = self._rom[0][value] if not self._ena else 0
		self.sevenSeg.b = self._rom[1][value] if not self._ena else 0
		self.sevenSeg.c = self._rom[2][value] if not self._ena else 0
		self.sevenSeg.d = self._rom[3][value] if not self._ena else 0
		self.sevenSeg.e = self._rom[4][value] if not self._ena else 0
		self.sevenSeg.f = self._rom[5][value] if not self._ena else 0
		self.sevenSeg.g = self._rom[6][value] if not self._ena else 0
	# end def

	@property
	def ena(self):
		return self._ena
	# end def

	@ena.setter
	def ena(self, value):
		self._ena = value
		self.bcd = self._bcd
	# end def

