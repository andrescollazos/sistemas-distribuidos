#!/usr/bin/env python
from socket import AF_INET, SOCK_DGRAM
import sys
import socket
import struct, time
import thread
from claseReloj import Reloj

# AJUSTAR RELOJ LOCAL DEL SISTEMA
relojSys = Reloj()
crearReloj = True
l = time.localtime()
relojSys.setHora(l.tm_hour, l.tm_min, l.tm_sec, 0)

# PREPARAR LOS PUERTOS PARA ESCUCHAR LAS PETICIONES
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 3000))
s.listen(10)

def mostrarHoraSys(reloj, sec):
    while 1:
        time.sleep(sec)
        print "##### ------> Hora local del maestro: ", reloj.retHora()

def connection(sc, address, reloj):
    while 1:
        data = sc.recv(1024)
        if data == "1":
            print "##### ------> CONEXION RECIBIDA"
            print str(address[0]) + ":" + str(address[1]) + ": Mande la hora de sus sistema..."
            #print "La hora del servidores es: ", reloj.retHora()
            respuesta = "correct"#reloj.retHora()
            sc.send(respuesta)
        elif len(data) == 12:
            print str(address[0]) + ":" + str(address[1]) + ": ", data

print "A la espera de las conexiones... "
while 1:
    if crearReloj:
        thread.start_new_thread(relojSys.tick,()) # INICIAR EL RELOJ
        thread.start_new_thread(mostrarHoraSys,(relojSys, 10)) # MOSTRAR HORA CADA n SEGUNDOS
        crearReloj = False
    #print "A la espera de las conexiones... "

    sc, addr = s.accept()
    #print "recibida conexion de la IP: " + str(addr[0]) + " puerto: " + str(addr[1])
    thread.start_new_thread(connection,(sc,addr, relojSys))

sc.close()
s.close()
