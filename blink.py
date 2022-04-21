#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ## ###############################################
# blink.py
#
# Author:  Mauricio Matamoros
# Licence: MIT
# Date:    2020.03.01
#
# Blinks a led on pin 32 using a Raspberry Pi
#
# ## ###############################################

# Import Raspberry Pi's GPIO control library
import RPi.GPIO as GPIO
# Imports sleep functon
from time import sleep
# Initializes virtual board (comment out for hardware deploy)
from virtualboards import run_led_board
run_led_board()

# Disable warnings
# GPIO.setwarnings(False)
# Set up Rpi.GPIO library to use physical pin numbers
GPIO.setmode(GPIO.BOARD)

# Set up pin no. 32 as output and default it to low
GPIO.setup(32, GPIO.OUT, initial=GPIO.LOW)


# Blink the led
while True: # Forever
	sleep(0.5)                 # Wait 500ms
	GPIO.output(32, GPIO.HIGH) # Turn led on
	sleep(0.5)                 # Espera 500ms
	GPIO.output(32, GPIO.LOW)  # Turn led off
