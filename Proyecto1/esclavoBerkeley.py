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
relojSys.setHora(l.tm_hour, l.tm_min+30, l.tm_sec, 0)

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
        print "Hora local del sistema: ", relojSys.retHora()
        time.sleep(0.050)
        s.send(relojSys.retHora())
        desface = s.recv(1024)
        desface = desface.split(":")
        if desface != ['correct']:
            for i, elem in enumerate(desface):
                #print "desface iteracion: ", int(elem)*int(desface[4])
                desface[i] = int(elem)*int(desface[4])
            #print "Desface respecto al maestro: ",
            #print desface[0], " horas ", desface[1], " minutos ", desface[2], " segundos ", desface[3], " milisegundos"

            relojSys.ajustarHora(desface[0], desface[1], desface[2], desface[3])

            print "La nueva hora del sistema es: ", relojSys.retHora()
            correcto = "incorrect"
        #break
    time.sleep(5)

s.close()
