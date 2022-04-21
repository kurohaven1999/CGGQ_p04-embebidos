#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# ## #############################################################
# virtualboards.py
#
# Author:  Mauricio Matamoros
# Licence: MIT
# Date:    2020.03.01
#
# Configures multiple boards to be run in a separate thread.
#
# ## #############################################################

import sys
import signal
from atexit import register
from threading import Barrier, Event, Thread
from threading import current_thread, main_thread
from board import LedsBoard, TemperatureBoard, DimmerBoard
from tkinter import Tk, mainloop
import RPi.GPIO as GPIO

_board = None
_board_type = None
_async_board_thread = None
_barrier = Event()# Barrier(2)


def _async_board_worker(*args, **kwargs):
	global _async_board_thread
	global _board

	if _board_type == 'leds':
		_board = LedsBoard()
		_board.connect(GPIO._io_pins)
	elif _board_type == 'temp':
		_board = TemperatureBoard(*args, **kwargs)
	elif _board_type == 'dimm':
		_board = DimmerBoard(*args, **kwargs)
	elif _board_type == 'ctrl':
		return
	else:
		return

	_barrier.set()

	try:
		print("Running GUI")
		mainloop()
	except:
		pass
	_async_board_thread = None
# end def



def _setup(*args, **kwargs):
	global _async_board_thread
	_async_board_thread = Thread(
		target = _async_board_worker,
		args = args,
		kwargs = kwargs)
	_async_board_thread.daemon = True
# end def



def _wait_board():
	_barrier.wait()
	# if current_thread() is main_thread():
	# 	signal.signal(signal.SIGINT, _board.close)
	# 	signal.signal(signal.SIGTERM, _board.close)
# end def



def _check_board():
	if (_board is not None) or (_async_board_thread is not None):
		raise RuntimeError("A board is already running")
# end def



def run_led_board():
	_check_board()
	_setup()

	global _board_type
	_board_type = "leds"
	_async_board_thread.start()
	_wait_board()
# end def



def run_temperature_board(r1=1, r2=1000, p8bits=False, freq=3):
	_check_board()
	_setup(r1=r1, r2=r2, p8bits=p8bits, freq=freq)
	# _setup()

	global _board_type
	_board_type = "temp"
	_async_board_thread.start()
	_wait_board()
# end def



def run_dimmer_board(address=10, freq=60):
	_check_board()
	_setup(address=address, frequency=freq)

	global _board_type
	_board_type = "dimm"
	_async_board_thread.start()
	_wait_board()
# end def



def run_tempcontrol_board():
	_check_board()
	_setup()

	global _board_type

	_async_board_thread.start()
	_wait_board()
# end def


