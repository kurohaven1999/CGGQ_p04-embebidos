#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ## #############################################################
# incandescent.py
#
# Author: Mauricio Matamoros
# Licence: MIT
# Date:
#
# ## #############################################################


import sys
import math
import struct

from os import _exit
from threading import Thread, Timer, Lock
from tkinter import *
from PIL import Image, ImageTk, ImageEnhance

from smbus2 import Vi2cSlave
from .__common import _img, _get_sprites, _set_kill_handler


class DimmerBoard(Vi2cSlave):
	def __init__(self, address=10, frequency=60):
		super().__init__(address)
		self._phase = 0
		self._phaselock = Lock()
		self._freq = frequency
		self._rms = 110
		self._data = [0, 0, 0, 0]

		# GUI
		self.gui = Tk(className=" Lamp Control Board")
		self.gui.bind("<<UpdateGUI>>", self._update_gui)
		self._io_pins = {}
		self.controls = {}
		for i in range(1, 28):
			self._io_pins[i] = None
		self._sprites = _get_sprites(_img("lightbulb.png"), 680, scale=0.17)
		self._initialize_components()
		_set_kill_handler(self.close)
		self.running = True
		self.phase = 1000
	# end def

	def __del__(self):
		_exit(1)
	# end def

	@property
	def freq(self):
		return self._freq
	# end def

	@property
	def vrms(self):
		return self._rms
	# end def

	@property
	def phase(self):
		self._phaselock.acquire()
		p = self._phase
		self._phaselock.release()
		return p
	# end def

	@phase.setter
	def phase(self, value):
		self._phaselock.acquire()
		max_phase = 1 / (self._freq * 2)
		self._phase = min(max_phase, max(0, value))
		self._phaselock.release()
	# end def

	@property
	def power(self):
		# return 100
		a = 2 * math.pi * self.freq * self.phase
		return (1 + math.cos(a))/ 0.02
	# end def


	def _initialize_components(self):
		# set window size
		# self.gui.geometry("510x270")
		self.gui.geometry("450x150")
		#set window color
		self.gui.configure(bg='#296e01')
		self.gui.protocol("WM_DELETE_WINDOW", self._on_closing)

		# Control instantiation
		self.strLineV = StringVar(self.gui)
		self.strLineF = StringVar(self.gui)
		self.strDataR = StringVar(self.gui)
		self.strPhase = StringVar(self.gui)
		self.strPower = StringVar(self.gui)

		# Validators

		self.lblLineV = Label(self.gui, anchor="w",
			bg="#296e01", fg="#e0e0e0",
			text="Voltaje (RMS):")
		self.txtLineV = Entry(self.gui, justify="right",
			width=10, state="readonly", textvariable=self.strLineV)

		self.lblLineF = Label(self.gui, anchor="w",
			bg="#296e01", fg="#e0e0e0",
			text="Frequency:")
		self.txtLineF = Entry(self.gui, justify="right",
			width=10, state="readonly", textvariable=self.strLineF)

		self.lblDataR = Label(self.gui, anchor="w",
			bg="#296e01", fg="#e0e0e0",
			text="Data received:")
		self.txtDataR = Entry(self.gui, justify="right",
			width=10, state="readonly", textvariable=self.strDataR)

		self.lblPhase = Label(self.gui, anchor="w",
			bg="#296e01", fg="#e0e0e0",
			text="Phase:")
		self.txtPhase = Entry(self.gui, justify="right",
			width=10, state="readonly", textvariable=self.strPhase)

		self.lblPower = Label(self.gui, anchor="w",
			bg="#296e01", fg="#e0e0e0",
			text="Power:")
		self.txtPower = Entry(self.gui, justify="right",
			width=10, state="readonly", textvariable=self.strPower)

		self.lblLampI = Label(self.gui, anchor="nw",
			bg="#e0e0e0", fg="#e0e0e0", height=140)

		# Control initialization
		self.lblLineV.grid(row=0, column=0, sticky="w", padx=2, pady=2)
		self.txtLineV.grid(row=0, column=1, sticky="w", padx=2, pady=2)
		self.lblLineF.grid(row=1, column=0, sticky="w", padx=2, pady=2)
		self.txtLineF.grid(row=1, column=1, sticky="w", padx=2, pady=2)
		self.lblDataR.grid(row=2, column=0, sticky="w", padx=2, pady=2)
		self.txtDataR.grid(row=2, column=1, sticky="w", padx=2, pady=2)
		self.lblPhase.grid(row=3, column=0, sticky="w", padx=2, pady=2)
		self.txtPhase.grid(row=3, column=1, sticky="w", padx=2, pady=2)
		self.lblPower.grid(row=4, column=0, sticky="w", padx=2, pady=2)
		self.txtPower.grid(row=4, column=1, sticky="w", padx=2, pady=2)

		self.lblLampI.grid(row=0, column=2, sticky="w", padx=75, pady=2,
		                   columnspan=2, rowspan=5)

		self.strLineV.set("{:0.0f}V".format(self._rms))
		self.strLineF.set("{:0.0f}Hz".format(self._freq))
		self.strPhase.set("{:0.1f}ms".format(self.phase))
		self.strPower.set("{:0.2f}%".format(self.power))

		self._update_gui()
	# end def

	def _on_closing(self):
		self.running = False
		self.disconnect()
		self.gui.destroy()
		self.gui.quit()
		sys.exit()
	# end def

	def _get_phase_image(self):
		ix = max(0, min(10, int(self.power/10)))
		if ix < 4:
			return ImageTk.PhotoImage(self._sprites[ix])
		img = Image.blend(
			self._sprites[4],
			self._sprites[8],
			alpha=min(1, 0.25 * ix -1))
		if ix > 8 :
			img = Image.alpha_composite(img, self._sprites[ix])
		return ImageTk.PhotoImage(img)
	# end def

	def _update_gui(self, e=None):
		self.strPhase.set("{:0.1f}ms".format(self.phase*1000))
		self.strPower.set("{:0.2f}%".format(self.power))
		sdata = "0x" + "".join("{:02x}".format(x) for x in self._data)
		self.strDataR.set(sdata)
		img = self._get_phase_image()
		self.lblLampI.configure(image=img)
		self.lblLampI.image = img
	#end def

	def close(self, *args):
		print("Shutting down GUI")
		self._on_closing()
	#end def

	def read(self):
		"""Master reads a byte stream from the slave"""
		self._data = struct.pack("<f", self.phase)
		return self._data
	#end def

	def write(self, value):
		"""Master writes byte stream to the slave"""
		self._data = value
		self.phase = struct.unpack("<f", value)[0]
		try:
			self.gui.event_generate("<<UpdateGUI>>", when="tail")
		except:
			pass
	#end def


