#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ## #############################################################
# __common.py
#
# Author:  Mauricio Matamoros
# Licence: MIT
# Date:    2020.03.01
#
# ## #############################################################


class Singleton(type):
	"""Singleton metaclass from https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python"""
	_instances = {}
	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
		return cls._instances[cls]
	#end def

def is_valid_address(value):
	"""Tells if the provided value is a valid I²C address"""
	return isinstance(value, int) and (value >= 0x00) and (value <= 0x7F)
#end def
