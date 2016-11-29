#!/usr/bin/env python
# coding=utf-8

from socket import AF_INET, SOCK_DGRAM
import sys
import socket
import struct, time
import thread
from claseReloj import Reloj

# HORA DESDE SERVIDOR NTP - ACTUANDO COMO CLIENTE
#client = socket.socket(AF_INET, SOCK_DGRAM)
#tiempo_init = time.time()
#client.sendto('\x1b' + 47 * '\0', ("pool.ntp.org", 123))
#msg, address = client.recvfrom(1024)
#tiempo_fin = time.time()

#t = struct.unpack("!12I", msg)[10] # CONVERTIR A HORA
#t = int(t - 2208988800L)
#horaI = time.ctime(t).replace(" ", " ")
#print "Hora recibida desde el servidor NTP: ", horaI
#print "Latencia (ms): ", int(1000*(tiempo_fin - tiempo_init))

# AJUSTAR RELOJ LOCAL DEL SERVER
#relojSys = Reloj()
crearReloj = True
#relojSys.setHora(int(horaI[11]+horaI[12]), int(horaI[14]+horaI[15]), int(horaI[17]+horaI[18]), int(1000*(tiempo_fin - tiempo_init)))

# MATRIZ DE INFORMACIÓN DE LAS PAGINAS
class Memoria():
    # CREAMOS UN CLASE MEMORIA QUE NOS PERMITE TENER EL MAPEO DE LAS LISTAS
    def __init__(self):
        self.mapa = {}

    # Metodo para imprimir el mapeo
    def __str__(self):
        return str(self.mapa)

    # Cuando se registra un nuevo nodo, creamos una llave en la memoria y registramos
    # sus paginas, si estas paginas no son originales de él, buscamos el propietario
    # y agregamos una dirección a la copia de la pagina
    def registrarPaginas(self, nodo, paginas):
        for i, elem in enumerate (paginas):
            paginas[i] = [elem]

        for i in paginas:
            if not (i[0][0] == nodo):
                # Comprar que el nodo con el que se compara si esta creado:
                try:
                    for j, elem in  enumerate (self.mapa[i[0][0]]):
                        if i[0] == elem[0]:
                            self.mapa[i[0][0]][j].append(nodo)
                except KeyError:
                    pass

        #print "MOSTRAR PAGINAS: ", paginas, type(paginas)
        self.mapa[nodo] = paginas

    def mostrarMapa(self):
        while 1:
            print self
            time.sleep(3)


memoria = Memoria()
#print "Cree mi memoria: ", memoria

# PREPARAR LOS PUERTOS PARA ESCUCHAR LAS PETICIONES
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', int(sys.argv[1])))
s.listen(10)

def connection(sc, address, memoria):
    #try:
    while True:
        data = sc.recv(1024)
        print "Data recibida: ", data
        if data > 0:
            #print "Recibí: ", data
            #print "La hora del servidores es: ", reloj.retHora()
            if not(len(data) == 1):
                if data[0] != 'E' and data[0] != 'L':
                    dataRec = data.split(";")
                    memoria.mapa.update({dataRec[0]:[]})
                    memoria.registrarPaginas(dataRec[0], dataRec[1:])
                    #respuesta = reloj.retHora()
                    sc.send("")
                else:
                    dataRec = data.split("-")
                    print dataRec
            else:
                sc.send('1')


while 1:
    if crearReloj:
        #thread.start_new_thread(relojSys.tick,())
        thread.start_new_thread(memoria.mostrarMapa, ())
        crearReloj = False
    print "A la espera de las conexiones... "
    sc, addr = s.accept()
    print "recibida conexion de la IP: " + str(addr[0]) + " puerto: " + str(addr[1])
    thread.start_new_thread(connection,(sc,addr, memoria))

sc.close()
s.close()
