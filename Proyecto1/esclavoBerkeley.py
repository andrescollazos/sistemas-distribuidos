#!/usr/bin/env python

import socket
import time
import thread
from claseReloj import Reloj

# CONEXION A SERVIDOR
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.connect(('localhost', 3000)) # ESTABLECER CONEXION CON EL SERVIDOR

# AJUSTAR RELOJ LOCAL DEL SISTEMA
relojSys = Reloj()
crearReloj = True
l = time.localtime()
relojSys.setHora(l.tm_hour, l.tm_min+3, l.tm_sec, 0)

#print "La hora del sistema antes de llamar al servidor: ", relojSys.mostrarHora()

continuar = True
while continuar:
    if crearReloj:
        thread.start_new_thread(relojSys.tick,())
        crearReloj = False

    #print "-------------------------------------------------------------"
    #print "La hora del sistema antes de llamar al servidor: ", relojSys.mostrarHora()

    tiempo_init = time.time()
    s.send("1") # EMPEZAR COMUNICACION CON EL MAESTRO
    correcto = s.recv(1024)
    tiempo_fin = time.time()

    if correcto == "correct":
        print "VOY A MANDAR MI HORA AL SERVIDOR..."
        s.send(relojSys.retHora())
        desface = s.recv(1024)

    '''
    print "La hora del sistema despues de llamar al servidor: ", relojSys.mostrarHora()
    print "La latencia cliente-servidor por la red (seg.): ", int(1000*(tiempo_fin - tiempo_init))
    print "La hora recibida del servidor: ", horaRecibida

    #### MODIFICAR HORA DEL CLIENTE
    #newHour = int(horaRecibida[0]+horaRecibida[1])
    #newMin = int(horaRecibida[3]+horaRecibida[4])
    #newSec = int(horaRecibida[6]+horaRecibida[7])
    #newMil = int(horaRecibida[9]+horaRecibida[10]+horaRecibida[11])
    #relojSys.setHora(newHour, newMin, newSec, newMil)
    #print "\n La nueva hora del cliente: ", relojSys.mostrarHora()

    ''''''
    resp= raw_input("Desea ajustar nuevamente la hora? (y/n): ")
    if resp == 'Y' or resp == 'y':
        continuar = True
    else:
        continuar = False
    ''''''
s.close()

'''
