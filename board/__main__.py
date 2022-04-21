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

from .ledsboard import LedsBoard
from .tboard import TemperatureBoard
from .dboard import DimmerBoard
from .tcboard import TempCtrlBoard
from tkinter import mainloop

def main():
	board = LedsBoard()
	# board = TemperatureBoard()
	# board = DimmerBoard()
	# board = TempCtrlBoard()
	mainloop()

if __name__ == '__main__':
	main()
