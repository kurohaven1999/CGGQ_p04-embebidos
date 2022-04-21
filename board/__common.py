#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ## #############################################################
# __common.py
#
# Author: Mauricio Matamoros
# Licence: MIT
# Date:
#
# ## #############################################################

import signal
import threading
from os import path
from PIL import Image, ImageTk, ImageEnhance


_img_path = "img"
_img_path = path.join(path.dirname(path.realpath(__file__)), _img_path)

def _img(file_name):
	return path.join(_img_path, file_name)

def _get_sprites(path, width, height=None, count=None, scale=1):
	sprites = []
	im = Image.open(path)
	w, h = im.size
	if not isinstance(height, int) or height < 1:
		height = h
	if not isinstance(count, int) or count < 1:
		count = int(w / width)
	for i in range(count):
		s = im.crop( (i * width, 0, (i+1) * width, height) )
		s = s.resize((int(width*scale), int(height*scale)), Image.ANTIALIAS)
		sprites.append(s)
	return sprites

def _set_kill_handler(handler):
	if threading.current_thread() is threading.main_thread():
		signal.signal(signal.SIGINT, handler)
		signal.signal(signal.SIGTERM, handler)