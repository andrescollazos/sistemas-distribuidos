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
relojSys.setHora(l.tm_hour, l.tm_min, l.tm_sec)

# PREPARAR LOS PUERTOS PARA ESCUCHAR LAS PETICIONES
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 3000))
s.listen(10)

def connection(sc, address, reloj):
    data = sc.recv(1024)
    while True:
        if data > 0:
            print "La hora del servidores es: ", reloj.retHora()
            respuesta = reloj.retHora()
            sc.send(respuesta)
        time.sleep(int(data))

def cambiarEstado(reloj, tiempo):
    while True:
        time.sleep(tiempo)
        cambio = raw_input("Estas activo? (yes/no): ")
        if cambio == 'Si' or cambio == 'SI' or cambio == 'si' or cambio == 'sI':
            reloj.inactivo = "activo"
        elif cambio == 'No' or cambio == 'NO' or cambio == 'no' or cambio == 'nO':
            reloj.inactivo = "inactivo"

def mostrarHora(reloj, tiempo):
    while True:
        time.sleep(tiempo)
        print "\nLa hora del servidor es: ", reloj.retHora()
        print "\nEstado de la terminal: ", reloj.inactivo

while 1:
    if crearReloj:
        thread.start_new_thread(relojSys.tick,())
        thread.start_new_thread(mostrarHora, (relojSys, 5))
        thread.start_new_thread(cambiarEstado, (relojSys, 7))
        crearReloj = False
    print "A la espera de las conexiones... "

    sc, addr = s.accept()
    print "recibida conexion de la IP: " + str(addr[0]) + " puerto: " + str(addr[1])
    thread.start_new_thread(connection,(sc,addr, relojSys))

sc.close()
s.close()
