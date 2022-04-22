#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ## #############################################################
# CGGQ_temperature.py
#
# Author: Cristian Gabriel Garcia Quezada
# Original by: Mauricio Matamoros
# Licence: MIT
# Date:    2022.04.19
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

HZ_cincuenta = [10.0, 9.166, 8.888 , 8.611,  8.055,  7.777, 7.5, 7.222, 6.944, 6.666, 6.388, 6.111, 5.555, 5.277,   #valores para
             5, 4.722, 4.166, 3.888, 3.333, 2.5, 0.000]                                                             #frecuencia 50hz

HZ_sesenta = [8.203, 7.688, 7.334, 7.030, 6.750, 6.487, 6.232 , 5.984, 5.738, 5.493, 5.245, 4.993, 4.734, 4.464,    #valores para
         4.179, 3.874, 3.538, 3.157, 2.696, 2.060, 0.000]                                                           #frecuencia 60hz

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

def powerf2ms(pw):                                                  #funcion para regular la frecuencia e intensidad manualmente
    hz = int(input("frecuencia de 50 o 60 HZ "))                    #solicitar una frecuencia de 50 o 60hz
    if hz == 50 or hz == 60:                                        #verificar que la frecuencia sean validas
        if hz == 50:                                                #para el caso de 50hz
            if pw % 5.0 == 0.0:                                     #si se cumple la condicion verificar
                return HZ_cincuenta[int(pw/5.0)]                    #en el arreglo y retornar el valor correspondiente
            else:                                                   #si no existe ese valor
                print("No existe valor")                            #mandar mensaje de error
                return 0                                            #regresar un 0
        elif hz == 60:                                              #para el caso de 50hz
            if pw % 6.0 == 0.0:                                     #si se cumple la condicion verificar
                return HZ_sesenta[int(pw/6.0)]                      #en el arreglo y retornar el valor correspondiente
            else:                                                   #si no existe ese valor
                print("No existe valor")                            #mandar mensaje de error
                return 0                                            #regresar un 0
    else:                                                           #Si las frecuencias no son correctas
        print("No es posible usar esa frecuencia ")                 #mandar mensaje de error
        return 0                                                    #regresar un 0
#end def
    

def main():                                                         #INICIO DEL PROGRAMA, FUNCION MAIN()
    # Runs virtual board (comment out for hardware deploy)
    run_dimmer_board(freq=60)                                       #comenzar con frecuencia de 60hz
    # # Shutdown lamp
    time.sleep(1)                                                   #tiempo de espera
    writePhase(1000/60)                                             #mostrar los valores
    while True:                 
        try:                                                        #inicio del manejo de interrupciones
            inten = int(input("Cambiara su intensidad 1=si 2=no 3=salir:  "))#menu inicial para seleccionar la opcion deseada
            if inten == 1:                                          #opcion 1
                print("proceso automatico")                         #inicio de proceso automatico
                hz = int(input("la frecuenci ira de 50 o 60 HZ "))  #eleccion de frecuencia con la que cambiara
                if hz == 50 or hz == 60:                            #verificacion de frecuencias de 50 o 60 hz
                    print("frecuencia aceptada ")                   #mensaje de aceptacion
                    if hz == 50:                                    #opcion frecuencia 50 hz
                        for x in HZ_cincuenta:                      #para recorrer los valores de la frecuencia de 50hz
                            writePhase(x)                           #escribe el valor de intensidad y tiempo
                            time.sleep(0.5)                         #tiempo de espera
                    elif hz == 60:                                  #opcion frecuencia 60 hz
                        for x in HZ_sesenta:                        #para recorrer los valores de la frecuencia de 60hz
                            writePhase(x)                           #escribe el valor de intensidad y tiempo
                            time.sleep(0.5)                         #tiempo de espera
                    writePhase(100.0)                               #resetea la intensidad para apagar foco
                else:                                               #en caso de que frecuencias invalidas
                    print("No es una frecuencia aceptada ")         #manda mensaje de error
                    main()                                          #retorna al menu inicial
     
            elif inten == 2:                                        #opcion 2
                print("se realizara de forma manual el proceso")    #inicio eleccion de proceso manual
                s = input("Enter power factor: ")                   #solicita el factor para incrementar intencidad
                if s in "qQxX":
                    return
                if (float(s) >= 0.0 and float(s) <= 100.0):         #verifica que este entre los rangos de factor correctos
                    pf = float(s)                                   #convierte el factor a flotante
                    writePhase(powerf2ms(pf))                       #escribe el valor acorde a la llamada de la funcion
                    time.sleep(1)                                   #tiempo de espera       
                    writePhase(100.0)                               #resetea todo y apaga foco
                else:                                               #si no entra dentro de los factores elegidos
                    print("valor incorrecto, escriba un valor entre 0.00 y 100.0")#mensaje indicando error
                    main()                                          #regreso a menu inicial

            elif inten == 3:                                        #opcion 3
                print("saliendo del programa")                      #salida del programa
                exit()                                              #salir
                
            else :                                                  #opcion 4
                print("no es una opcion valida")                    #indica que no se eligio opcion valida
                main()                                              #redirecciona al meni inicia
            
        except KeyboardInterrupt:                                   #manejos de interrupcion
            return
        except:
            continue
#end def

if __name__ == '__main__':
	main()
