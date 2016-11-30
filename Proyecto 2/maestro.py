#!/usr/bin/env python
# coding=utf-8

from socket import AF_INET, SOCK_DGRAM
import sys
import socket
import thread
import time

iniciarProceso = True

# MATRIZ DE INFORMACIÓN DE LAS PAGINAS
class Memoria():
    # CREAMOS UN CLASE MEMORIA QUE NOS PERMITE TENER EL MAPEO DE LAS LISTAS
    def __init__(self):
        self.mapa = {}
        self.puertos = {}
        self.usados = []
        self.contador = 5000

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

        self.mapa[nodo] = paginas

    def mostrarMapa(self):
        while 1:
            print "DATOS DE INFORMACIÓN SOBRE EL ESTADO DE LA MEMORIA: "
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
            if data[0] != 'E' and data[0] != 'L':
                dataRec = data.split(";")
                memoria.mapa.update({dataRec[0]:[]})
                memoria.registrarPaginas(dataRec[0], dataRec[1:])
                #respuesta = reloj.retHora()
                sc.send(str(memoria.contador))
                memoria.puertos.update({dataRec[0]:memoria.contador})
                memoria.contador = memoria.contador + 10
            else:
                dataRec = data.split("-")
                print dataRec
                if len(dataRec) == 4:
                    if dataRec[0] == 'E':
                        print "---------------------"
                        print "Pagina modificada: ", dataRec[1]
                        try:
                            memoria.usados.remove(dataRec[1])
                            #print "Los siguientes nodos deben actualizar sus paginas: "

                            # Vector que contiene los nodos con una copia de la pagina:
                            actualizarse = [dataRec[1][0]] # Propietario

                            # Buscar los nodos que contienen una copia de la pagina
                            for i in memoria.mapa[dataRec[1][0]]:
                                if i[0] == dataRec[1]:
                                    copias = i[1:] # Crear un vector para las copias

                            for i in copias:
                                actualizarse.append(i) # Agregar los elementos del vector
                                                       # De las copias al vector de actualización
                            #print actualizarse
                            for i in actualizarse:
                                to = memoria.puertos[i]
                                actualizar = socket.socket()
                                actualizar.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                                actualizar.connect(('localhost', to))

                                mensaje = "A-"+ dataRec[1] + "-" + dataRec[2] + "-" + dataRec[3]
                                actualizar.send(mensaje)
                                actualizar.close()
                        except:
                            pass
                    elif dataRec[0] == 'L':
                        try:
                            memoria.usados.remove(dataRec[1])
                        except:
                            pass
                elif len(dataRec) == 2:
                    # AGREGAR PAGINAS USADAS:
                    if not(dataRec[1] in memoria.usados):
                        memoria.usados.append(dataRec[1])
                        sc.send('1')
                    else:
                        sc.send('0')

while 1:
    if iniciarProceso:
        thread.start_new_thread(memoria.mostrarMapa, ())
        iniciarProceso = False
    print "A la espera de las conexiones... "
    sc, addr = s.accept()
    print "recibida conexion de la IP: " + str(addr[0]) + " puerto: " + str(addr[1])
    thread.start_new_thread(connection,(sc,addr, memoria))

sc.close()
s.close()
