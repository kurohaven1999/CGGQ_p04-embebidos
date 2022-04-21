#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ## #############################################################
# vi2cbus.py
#
# Author:  Mauricio Matamoros
# Licence: MIT
# Date:    2020.03.01
#
# Implements a virtual I²C bus
#
# ## #############################################################

from .__common import *

class Vi2cBus(metaclass=Singleton):

	def __init__(self):
		self._slaves = {}
		print("Virtual I²C bus ready.")

	def _tether(self, slave):
		if not isinstance(slave, Vi2cSlave):
			raise TypeError("Expected instance of Vi2cSlave")
		if slave.address in self._slaves:
			raise ValueError("Slave address already in use")
		self._slaves[slave.address] = slave
		print("Slave {} connected to I²C bus.".format(slave.address))
	# end def

	def _untether(self, slave):
		if not isinstance(slave, Vi2cSlave):
			raise TypeError("Expected instance of Vi2cSlave")
		if slave.address in self._slaves:
			del self._slaves[slave.address]
		print("Slave {} disconnected from I²C bus.".format(slave.address))
	# end def

	def read(self, address, count):
		if not address in self._slaves:
			print("Slave 0x{:02x} is not connected".format(msg.addr), file = sys.stderr)
			return bytearray([0] * count)

		buff = self._slaves[address].read()
		if isinstance(buff, bytearray) and len(buff) == count:
			return buff
		if not isinstance(buff, list):
			buff = list(buff)
		if (count > 0) and (len(buff) > count):
			return bytearray(buff[:count])
		while len(buff) < count:
			buff.append(0)
		return bytearray(buff)
	# end def

	def write(self, address, buffer):
		if not address in self._slaves:
			print("Slave 0x{:02x} is not connected".format(msg.addr), file = sys.stderr)
			return
		if buffer and len(buffer) > 0:
			self._slaves[address].write(buffer)
	# end def

	def __getitem__(self, key):
		if not is_valid_address(key):
			raise TypeError("Expected address (7bit integer)")

		return self._slaves[key]
	# end def

	def __contains__(self, key):
		if not is_valid_address(key):
			raise TypeError("Expected address (7bit integer)")

		return key in self._slaves
	#end def

# end class


class Vi2cSlave:
	def __init__(self, address):
		if not is_valid_address(address):
			raise TypeError("Expected address (7bit integer)")

		self._bus = Vi2cBus()
		self._address = address
		self._bus._tether(self)
	#end def

	def __del__(self):
		self.disconnect()
	#end def

	@property
	def address(self):
		return self._address
	#end def

	def read(self):
		"""Reads a byte stream from the slave"""
		raise NotImplementedError()
	#end def

	def write(self, value):
		"""Writes byte stream to the slave"""
		raise NotImplementedError()
	#end def
	#
	def disconnect(self):
		self._bus._untether(self)
		self._bus = None
		self._address = None

# end class



