#!/usr/bin/env python
# coding=utf-8
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

# RECIBIR PARAMETROS DE CONFIGURACION:
arch = open("users.txt", "r+")
puerto_peticion = arch.read().split(",")
puerto_peticion.pop()

try:
    puerto_escucha = int(sys.argv[1])
    relojSys.peticion = 0
    tipoUser = 0
    arch.write(str(puerto_escucha)+",")
    arch.seek(0)
    puerto_peticion = arch.read().split(",")

    # PREPARAR LOS PUERTOS PARA ESCUCHAR LAS PETICIONES
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', int(puerto_escucha)))
    s.listen(10)
    retardo = int(sys.argv[2])

except ValueError:
    tipoUser = 'cliente'
    relojSys.peticion = sys.argv[1]
    una_vez = True # MOSTRAR MENSAJE DE BIENVENIDA UNA SOLA VEZ:


def post(sc, address, reloj):
    data = sc.recv(1024)
    if len(data) > 0:
        if reloj.inactivo == "activo":
            print ">> Puedo resolver la peticion: ", data
            respuesta = data+"R/Solucionado"
            sc.send(respuesta)
        else:
            print">> No puedo resolver la peticion: ", data
            sc.send("")
    else:
        sc.send("")

def get(addr, puerto, reloj):
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.connect((addr, puerto))

    # TOMAR TIEMPO:
    tiempo_init = time.time()
    s.send(reloj.peticion) # CADA CUANTOS SEGUNDOS PIDE LA HORA
    respuesta = s.recv(1024)
    tiempo_fin = time.time()

    if len(respuesta) > 0 and not(reloj.peticion_solucionada):
        print ">> {0}:{1} dice {2}".format(addr, puerto, respuesta)
        reloj.peticion_solucionada = True



def cambiarEstado(reloj, tiempo):
    while True:
        time.sleep(0.003)
        print "\n>> Nuevo estado de la terminal: ", reloj.inactivo
        time.sleep(tiempo)
        activo = raw_input(">> Estas INACTIVO (si/no)?")
        if activo == 'si' or activo == 'sI' or activo == 'Si' or activo == 'SI':
            reloj.inactivo = 'inactivo'
        else:
            reloj.inactivo = 'activo'

def mostrarHora(reloj, tiempo):
    while True:
        time.sleep(tiempo)
        print "\n>> La hora de la estacion es: {0} estado: {1}".format(reloj.retHora(), reloj.inactivo)

while 1:
    if crearReloj:
        thread.start_new_thread(relojSys.tick,())
        thread.start_new_thread(mostrarHora, (relojSys, 10))
        thread.start_new_thread(cambiarEstado, (relojSys, 5))
        crearReloj = False
    if not(tipoUser):
        print ">> A la espera de las conexiones... "

        sc, addr = s.accept()
        time.sleep(retardo)
        print ">> recibida conexion de la IP: " + str(addr[0]) + " puerto: " + str(addr[1])
        thread.start_new_thread(post,(sc, addr, relojSys))
    else:
        if una_vez:
            print "NECESITO RESOLVER LA PETICION: ", relojSys.peticion
            una_vez = False

            print "Le mandaré solicitudes a: "
            print puerto_peticion
            for i, elem in enumerate(puerto_peticion):
                thread.start_new_thread(get, ('localhost', int(elem), relojSys))

sc.close()
s.close()
