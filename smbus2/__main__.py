#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ## #############################################################
# board.py
#
# Author:  Mauricio Matamoros
# Licence: MIT
# Date:    2020.03.01
#
# ## #############################################################

from . import smbus as smbus2
from .vi2cbus import Vi2cSlave
import struct
SLAVE_ADDR = 0x0a

class TestSlave(Vi2cSlave):
	def __init__(self):
		super().__init__(SLAVE_ADDR)

	def read(self):
		return [0, 0, 69, 0]

	def write(self, value):
		print("Write:", value)

slave = TestSlave()

def read(i2c):
	# Creates a message object to read 4 bytes from SLAVE_ADDR
	msg = smbus2.i2c_msg.read(SLAVE_ADDR, 4)
	i2c.i2c_rdwr(msg) # Performs read
	if msg.len > 0:
		# if we got data, unpack and print
		val = struct.unpack('<f', msg.buf)
		print('Received: {} = {}'.format(msg.buf, val))
	else:
		print('No data received')

def write(i2c):
	val = 100
	data = struct.pack('<f', val) # Packs number as float
	# Creates a message object to write 4 bytes from SLAVE_ADDR
	msg = smbus2.i2c_msg.write(SLAVE_ADDR, data)
	i2c.i2c_rdwr(msg) # Performs write

def main():
	i2c = smbus2.SMBus(1)
	read(i2c)
	write(i2c)

if __name__ == '__main__':
	main()
