#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ## #############################################################
# temperature.py
#
# Author:  Mauricio Matamoros
# Licence: MIT
# Date:    2020.03.01
# 
# Reads temperature from a LM35 interfaced via an Arduino ADC
# connected as I2C slave.
#
# ## #############################################################

import smbus2
import struct
import time

# Initializes virtual board (comment out for hardware deploy)
from virtualboards import run_temperature_board

# Arduino's I2C device address
SLAVE_ADDR = 0x0A # I2C Address of Arduino

# Name of the file in which the log is kept
LOG_FILE = './temp.log'

# Initialize the I2C bus;
# RPI version 1 requires smbus.SMBus(0)
i2c = smbus2.SMBus(1)

def readTemperature():
	"""Reads a temperature bytes from the Arduino via I2C"""
	try:
		msg = smbus2.i2c_msg.read(SLAVE_ADDR, 1)
		i2c.i2c_rdwr(msg)
		data = list(msg)
		temp = struct.unpack('<B', msg.buf)[0]
		print('Received ADC temp value: {} = {:0.2f}'.format(data, temp))
		return temp
	except:
		return None
#end def

def log_temp(temperature):
	try:
		with open(LOG_FILE, 'a') as fp:
			fp.write('{} {:0.2f}C\n'.format(
				time.strftime("%Y.%m.%d %H:%M:%S"),
				temperature
			))
	except:
		return
#end def

def main():
	# Runs virtual board (comment out for hardware deploy)
	run_temperature_board(r1=1, r2=10000, p8bits=True)
	time.sleep(1)

	while True:
		try:
			cTemp = readTemperature()
			log_temp(cTemp)
			time.sleep(1)
		except KeyboardInterrupt:
			return
#end def

if __name__ == '__main__':
	main()
