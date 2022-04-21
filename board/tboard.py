#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ## #############################################################
# tcboard.py
#
# Author:  Mauricio Matamoros
# Licence: MIT
# Date:    2020.03.01
#
# ## #############################################################

import re
import sys
import time
import random
import struct
from os import path, _exit
from threading import Thread, Timer, Lock
from tkinter import *

from PIL import Image, ImageTk, ImageEnhance

from .led import LED
from .sevenseg import SevenSeg
from .bcd7seg import BCD7Seg
from .__common import _img, _get_sprites, _set_kill_handler
from smbus2 import Vi2cSlave

def _format_r(r):
	mod = "k"
	if r < 1:
		r*=1000
		mod = ""
	elif r >= 1000:
		r/=1000
		mod = "M"
	elif r >= 1000000:
		r/=1000000
		mod = G
	return "{:.0f}{}Ω".format(r, mod)

class TemperatureBoard(Vi2cSlave):
	def __init__(self, r1=1, r2=100000, p8bits=False, freq=10):
		super().__init__(10)
		self._templock = Lock()
		self._temp = 0
		self._data = None
		# Calculate Vref+
		self._r1 = r1
		self._r2 = r2
		self._vref = 5 * r2 / (r2+r1)
		# ADC bits
		self._bits = 8 if p8bits else 10
		# Conversion factor: 1°C = 0.01V, range 0–150
		self._factor = 0.01 * (2**self._bits) / self._vref
		# ADC frequency
		self._freq = freq


		# GUI
		random.seed(time.time())
		self.gui = Tk(className=" Temperature Sensor Board")
		self.gui.bind("<<UpdateData>>", self._update_data_sent)
		self._io_pins = {}
		self.controls = {}
		for i in range(1, 28):
			self._io_pins[i] = None
		self._initialize_components()
		self._setup_timer()
		_set_kill_handler(self.close)
		self.running = True
	# end def

	def __del__(self):
		_exit(1)
	# end def

	def _initialize_components(self):
		# set window size
		self.gui.geometry("450x120")
		#set window color
		self.gui.configure(bg="#000000")
		self.gui.protocol("WM_DELETE_WINDOW", self._on_closing)

		# Control instantiation
		self.strTempR = StringVar(self.gui)
		self.strTempS = StringVar(self.gui)
		self.strDataS = StringVar(self.gui)
		self.strSFreq = StringVar(self.gui)
		self.strADCR1 = StringVar(self.gui)
		self.strADCR2 = StringVar(self.gui)
		self.strADCVR = StringVar(self.gui)
		self.strADCbt = StringVar(self.gui)

		# Validators
		validatetemp = self.gui.register(self._validatetemp)
		validatefreq = self.gui.register(self._validatefreq)

		self.lblTempR = Label(self.gui, anchor="w",
			bg="#000000", fg="#e0e0e0",
			text="Temperature (real):")
		self.txtTempR = Entry(self.gui, justify="right",
			width=10, textvariable=self.strTempR,
			validate='all', validatecommand=(validatetemp, '%P'))

		self.lblTempS = Label(self.gui, anchor="w",
			bg="#000000", fg="#e0e0e0",
			text="Temperature (sensor):")
		self.txtTempS = Entry(self.gui, justify="right",
			width=10, state="readonly", textvariable=self.strTempS)

		self.lblSFreq = Label(self.gui, anchor="w",
			bg="#000000", fg="#e0e0e0",
			text="ADC Frequency:")
		self.txtSFreq = Entry(self.gui, justify="right",
			width=10, textvariable=self.strSFreq,
			validate='all', validatecommand=(validatefreq, '%P'))

		self.lblDataS = Label(self.gui, anchor="w",
			bg="#000000", fg="#e0e0e0",
			text="Data sent:")
		self.txtDataS = Entry(self.gui, justify="right",
			width=10, state="readonly", textvariable=self.strDataS)



		self.lblADCR1 = Label(self.gui, anchor="w",
			bg="#000000", fg="#e0e0e0",
			text="ADC R1:")
		self.txtADCR1 = Entry(self.gui, justify="right",
			width=10, state="disabled", textvariable=self.strADCR1)

		self.lblADCR2 = Label(self.gui, anchor="w",
			bg="#000000", fg="#e0e0e0",
			text="ADC R2:")
		self.txtADCR2 = Entry(self.gui, justify="right",
			width=10, state="disabled", textvariable=self.strADCR2)

		self.lblADCVR = Label(self.gui, anchor="w",
			bg="#000000", fg="#e0e0e0",
			text="ADC Vref+:")
		self.txtADCVR = Entry(self.gui, justify="right",
			width=10, state="disabled", textvariable=self.strADCVR)

		self.lblADCbt = Label(self.gui, anchor="w",
			bg="#000000", fg="#e0e0e0",
			text="ADC bits:")
		self.txtADCbt = Entry(self.gui, justify="right",
			width=10, state="disabled", textvariable=self.strADCbt)

		# Control initialization
		self.lblTempR.grid(row=0, column=0, sticky="w", padx=2, pady=2)
		self.txtTempR.grid(row=0, column=1, sticky="w", padx=2, pady=2)
		self.lblSFreq.grid(row=1, column=0, sticky="w", padx=2, pady=2)
		self.txtSFreq.grid(row=1, column=1, sticky="w", padx=2, pady=2)
		self.lblTempS.grid(row=2, column=0, sticky="w", padx=2, pady=2)
		self.txtTempS.grid(row=2, column=1, sticky="w", padx=2, pady=2)
		self.lblDataS.grid(row=3, column=0, sticky="w", padx=2, pady=2)
		self.txtDataS.grid(row=3, column=1, sticky="w", padx=2, pady=2)

		self.lblADCR1.grid(row=0, column=2, sticky="w", padx=(30, 2), pady=2)
		self.txtADCR1.grid(row=0, column=3, sticky="w", padx=( 2, 2), pady=2)
		self.lblADCR2.grid(row=1, column=2, sticky="w", padx=(30, 2), pady=2)
		self.txtADCR2.grid(row=1, column=3, sticky="w", padx=( 2, 2), pady=2)
		self.lblADCVR.grid(row=2, column=2, sticky="w", padx=(30, 2), pady=2)
		self.txtADCVR.grid(row=2, column=3, sticky="w", padx=( 2, 2), pady=2)
		self.lblADCbt.grid(row=3, column=2, sticky="w", padx=(30, 2), pady=2)
		self.txtADCbt.grid(row=3, column=3, sticky="w", padx=( 2, 2), pady=2)

		self.strTempR.set("22.0")
		self.strTempS.set("0.0")
		self.strSFreq.set(self._freq)
		self.strADCR1.set(_format_r(self._r1))
		self.strADCR2.set(_format_r(self._r2))
		self.strADCVR.set("{:.2f}V".format(self._vref))
		self.strADCbt.set(self._bits)
	# end def

	def _on_closing(self):
		self.running = False
		self.timer.cancel()
		self.timer = None
		self.disconnect()
		self.gui.destroy()
		self.gui.quit()
		sys.exit()
	# end def

	def _update_status(self):
		pass
	# end def


	def _validatetemp(self, value):
		try:
			temp = float(value)
			if temp >= 0 and temp <= 150:
				return True
			return False
		except:
			return False

	def _validatefreq(self, value):
		try:
			freq = int(value)
			if freq > 0 and freq <= 100:
				return True
			return False
		except:
			return False

	def _setup_timer(self):
		try:
			delay = 1 / float(self.strSFreq.get())
		except:
			delay = 0.1
		self.timer = Timer(delay, self._timer_task)
		self.timer.daemon = True
		self.timer.start()

	def _timer_task(self):
		try:
			temp = float(self.strTempR.get())
		except:
			if self.running:
				self._setup_timer()
			return

		temp += 0.01 * random.randint(-100, 100)
		temp = max(min(temp, 150), 0)
		self._templock.acquire()
		self._temp = temp
		self._templock.release()

		try:
			self.strTempS.set("{:.2f}".format(temp))
		except:
			if self.running:
				self._setup_timer()
			return

		if self.running:
			self._setup_timer()
	# end def

	def _update_data_sent(self, event):
		sdata = "0x" + "".join("{:02x}".format(x) for x in self._data)
		self.strDataS.set(sdata)

	def close(self, *args):
		print("Shutting down GUI")
		self._on_closing()

	def read(self):
		"""Master reads a byte stream from the slave"""
		self._templock.acquire()
		# Get digital value of temperature
		adcval = int(self._temp * self._factor)
		self._templock.release()

		# Encode data (H = 2 byte unsigned short, f = 4 byte float)
		# self._data = struct.pack("<f", self._temp)
		adcval = max(min(adcval, 2**self._bits -1), 0)
		fmt = "<Q"
		if self._bits <= 8:
			fmt = "<B"
		elif self._bits <= 16:
			fmt = "<H"
		elif self._bits <= 32:
			fmt = "<I"
		self._data = struct.pack(fmt, adcval)

		try:
			self.gui.event_generate("<<UpdateData>>", when="tail")
		except:
			pass
		return self._data
	#end def

	def write(self, value):
		"""Master writes byte stream to the slave"""
		# Sets the ADC frequency (capped to 100Hz)
		return
		freq = struct.unpack('<f', value)
		if freq > 100:
			freq = 100
		elif freq < 1:
			freq = 1
		freq = int(freq)
		self.strSFreq.set(freq)

	#end def

