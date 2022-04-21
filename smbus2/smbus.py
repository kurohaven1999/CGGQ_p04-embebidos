#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ## #############################################################
# board.py
#
# Author:  Mauricio Matamoros
# Licence: MIT
# Date:    2020.03.01
#
# Replicates smbus module for i²C communication with the
# simulated board.
#
# ## #############################################################

import sys
from .vi2cbus import Vi2cBus, Vi2cSlave
# from . import vi2cbus

class SMBus:
	def __init__(self, bus=None, force=False):
		self._bus = Vi2cBus()
		self.open(bus)
	#end def

	def block_process_call(self, i2c_addr, register, data, force=None):
		"""
		NOT IMPLEMENTED

		Executes a SMBus Block Process Call, sending a variable-size data block and receiving another variable-size response

		Parameters:
			— i2c_addr(int) – i2c address
			— register(int) – Register to read/write to
			— data(list) – List of bytes
			— force(Boolean) –

		Returns:
			List of bytes
 			Return type list
		"""
		raise NotImplementedError()



	def close(self):
		"""
		Close the i2c connection.
		"""
		pass



	def enable_pec(self, enable=True):
		"""
		Enable/Disable PEC (Packet Error Checking) - SMBus 1.1 and later

		Parameters:
			— enable(Boolean) –
		"""
		self.pec = enable



	def i2c_rdwr(self, *i2c_msgs):
		"""
		Combine a series of i2c read and write operations in a single transaction (with repeated start bits but nostop bits in between).
		This method takes i2c_msg instances as input, which must be created first withi2c_msg.read() or i2c_msg.write().

		Parameters:
			— i2c_msgs(i2c_msg) – One or more i2c_msg class instances.


		Return type None
		"""
		for msg in i2c_msgs:
			if not isinstance(msg, i2c_msg):
				raise TypeError("Expected i2c_msg class instances")

			if msg.flags & 1:
				# read operation
				msg._buf = self._bus.read(msg.addr, msg.len)
			else:
				# write operation
				self._bus.write(msg.addr, msg.buf)
		return None
	# end def

	def open(self, bus):
		"""
		Open a given i2c bus.

		Parameters:
			— bus(int or str) – i2c bus number (e.g.  0 or 1) or an absolute file path (e.g.‘/dev/i2c-42’).
			— Raises TypeError– if type(bus) is not in (int, str)
		"""
		if not isinstance(bus, str) and not isinstance(bus, int):
			raise TypeError("Expected i2c bus number (e.g.  0 or 1) or an absolute file path (e.g.‘/dev/i2c-42’)")
		if bus != 1:
			raise ValueError("Unsupported device")



	@property
	def pec(self):
		"""
		Get and set SMBus PEC. 0 = disabled (default), 1 = enabled.
		"""
		return self._pec

	@pec.setter
	def pec(self, value):
		self._pec = 1 if value else 0


	def process_call(self, i2c_addr, register, value, force=None):
		"""
		NOT IMPLEMENTED

		Executes a SMBus Process Call, sending a 16-bit value and receiving a 16-bit response

		Parameters:
			—i2c_addr(int) – i2c address
			—register(int) – Register to read/write to
			—value(int) – Word value to transmit
			—force(Boolean) –

		Return type int
		"""
		raise NotImplementedError()



	def read_block_data(self, i2c_addr, register, force=None):
		"""
		NOT IMPLEMENTED

		Read a block of up to 32-bytes from a given register.Parameters
			—i2c_addr(int) – i2c address
			—register(int) – Start register
			—force(Boolean) –ReturnsList of bytes

		Return type list
		"""
		if register != 0:
			raise ValueError("Unsupported register")
		return self._bus.read(i2c_addr, -1)



	def read_byte(self, i2c_addr, force=None):
		"""
		NOT IMPLEMENTED

		Read a single byte from a device.

		Parameters:
			—i2c_addr(int) – i2c address
			—force(Boolean) –

		Returns:
			Read byte value
			Return type int
		"""
		return self._bus.read(i2c_addr, 1)[0]



	def read_byte_data(self, i2c_addr, register = 0, force=None):
		"""
		Read a single byte from a designated register.

		Parameters:
			—i2c_addr(int) – i2c address
			—register(int) – Register to read
			—force(Boolean) –

		Returns:
			Read byte value
			Return type int
		"""
		if register != 0:
			raise ValueError("Unsupported register")
		return self._bus.read(i2c_addr, 1)[0]



	def read_i2c_block_data(self, i2c_addr, register = 0, length = -1, force=None):
		"""
		Read a block of byte data from a given register.

		Parameters:
			—i2c_addr(int) – i2c address
			—register(int) – Start register
			—length(int) – Desired block length
			—force(Boolean) –

		Returns:
			List of bytes
			Return type list
		"""
		if register != 0:
			raise ValueError("Unsupported register")

		return self._bus.read(i2c_addr, length)



	def read_word_data(self, i2c_addr, register, force=None):
		"""
		NOT IMPLEMENTED

		Read a single word (2 bytes) from a given register.

		Parameters:
			—i2c_addr(int) – i2c address
			—register(int) – Register to read
			—force(Boolean) –

		Returns:
			2-byte word
			Return type int
		"""
		raise NotImplementedError()




	def write_block_data(self, i2c_addr, register, data, force=None):
		"""
		NOT IMPLEMENTED

		Write a block of byte data to a given register.

		Parameters:
			—i2c_addr(int) – i2c address
			—register(int) – Start register
			—data(list) – List of bytes
			—force(Boolean) –

		Return type None
		"""
		if register != 0:
			raise ValueError("Unsupported register")
		if not isinstance(data, bytearray):
			raise TypeError("Data must be a bytearray")
		self._bus.write(i2c_addr, data)



	def write_byte(self, i2c_addr, value, force=None):
		"""
		Write a single byte to a device.

		Parameters:
			—i2c_addr(int) – i2c address
			—value(int) – value to write
			—force(Boolean) –
		"""
		if not isinstance(data, int):
			raise TypeError("Data must be a byte")
		if data < 0 or data > 255:
			raise ValueError("Data must be a byte")

		data = bytearray([value])
		self._bus.write(i2c_addr, data)



	def write_byte_data(self, i2c_addr, register, value, force=None):
		"""
		NOT IMPLEMENTED

		Write a byte to a given register.

			Parameters:
			—i2c_addr(int) – i2c address
			—register(int) – Register to write to
			—value(int) – Byte value to transmit
			—force(Boolean) –

		Return type None
		"""
		if register != 0:
			raise ValueError("Unsupported register")

		self.write_byte(i2c_addr, value, force)



	def write_i2c_block_data(self, i2c_addr, register, data, force=None):
		"""
		NOT IMPLEMENTED

		Write a block of byte data to a given register.

		Parameters:
			—i2c_addr(int) – i2c address
			—register(int) – Start register
			—data(list) – List of bytes
			—force(Boolean) –
		Return type None
		"""
		if register != 0:
			raise ValueError("Unsupported register")
		return self._bus.write(i2c_addr, data)



	def write_quick(self, i2c_addr, force=None):
		"""
		NOT IMPLEMENTED

		Perform quick transaction.
		Throws IOError if unsuccessful

		Parameters:
			— param i2c_addr — i2c address
			— force: Boolean
		"""
		self._bus.write(i2c_addr, bytearray(0))



	def write_word_data(self, i2c_addr, register, value, force=None):
		"""
		NOT IMPLEMENTED

		Write a single word (2 bytes) to a given register.
		Parameters:
			—i2c_addr(int) – i2c address
			—register(int) – Register to write to
			—value(int) – Word value to transmit
			—force(Boolean) –
			Return type None
		"""
		raise NotImplementedError()





class i2c_msg:
	"""As defined ini2c.h."""

	def __init__(self):
		self._addr = 0
		self._buf = bytearray(0)
		self._flags = 0
		self._len = 0

	@property
	def addr(self):
		return self._addr

	@property
	def buf(self):
		return self._buf

	@property
	def flags(self):
		return self._flags


	@property
	def len(self):
		return self._len

	def __iter__(self):
		if self._buf is None:
			return iter(())
		return self._buf.__iter__()

	def __next__(self):
		if self._buf is None:
			return iter(())
		return self._buf.__next__()

	@staticmethod
	def read(address, length):
		"""
		Prepares an i2c read transaction.

		Parameters:
			—address – Slave address.
			—length  – Number of bytes to read.

		Returns:
			New i2c_msg instance for read operation.
			Return type i2c_msg
		"""
		msg = i2c_msg()
		msg._addr = address
		msg._flags = 1
		msg._len = length

		return msg

	@staticmethod
	def write(address, buf):
		"""
		Prepares an i2c write transaction.

		Parameters:
		—address (int) – Slave address.
		—buf (list)    – Bytes to write. Either list of values or str.

		Returns:
			New i2c_msg instance for write operation.
			Return typei2c_msg
		"""
		msg = i2c_msg()
		msg._addr = address
		if isinstance(buf, str):
			msg._buf = bytearray(buf.encode())
		elif isinstance(buf, int) or isinstance(buf, float):
			raise ValueError("Expected a packed bytearray object")
		else:
			msg._buf = buf
		msg._len = len(msg._buf)
		return msg
