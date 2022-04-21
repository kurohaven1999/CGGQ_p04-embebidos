#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ## #############################################################
# temperature.py
#
# Author:  Mauricio Matamoros
# Licence: MIT
# Date:    2020.03.01
# 
# Dimms an incandescent lamp using an Arduino connected
# as I2C slave. The output power is set by shifting the
# phase angle the specified amount of milliseconds from
# the last zero-cross on the AC voltaje line.
#
# ## #############################################################

import smbus2
import struct
import time

# Initializes virtual board (comment out for hardware deploy)
from virtualboards import run_dimmer_board

# Arduino's I2C device address
SLAVE_ADDR = 0x0A # I2C Address of Arduino

# Initialize the I2C bus;
# RPI version 1 requires smbus.SMBus(0)
i2c = smbus2.SMBus(1)

def writePhase(delay):
	"""Writes the delay phase in milliseconds to the Arduino via I2C"""
	try:
		data = struct.pack('<f', delay/1000.0)
		msg = smbus2.i2c_msg.write(SLAVE_ADDR, data)
		i2c.i2c_rdwr(msg)
		print('Written phase delay: {:0.5f} ({:0.1f}ms)'.format(delay/1000.0, delay))
	except Exception as ex:
		raise ex
#end def

def powerf2ms(pw):
	# Student's code here
	return pw
#end def

def main():
	# Runs virtual board (comment out for hardware deploy)
	run_dimmer_board(freq=60)
	# Shutdown lamp
	time.sleep(1)
	writePhase(1000/60)

	while True:
		try:
			s = input("Enter power factor: ")
			if s in "qQxX":
				return
			pf = float(s)
			writePhase(powerf2ms(pf))
		except KeyboardInterrupt:
			return
		except:
			continue
#end def

if __name__ == '__main__':
	main()
