# -*- coding: utf-8 -*

from socket import AF_INET, SOCK_DGRAM
import sys
import socket
import struct, time
import thread

class Grafo(object):
    def __init__(self):
        self.relaciones = {}
        self.estado = "Sin bloqueo"
    def __str__(self):
        return str(self.relaciones)

    def agregar(self, elemento):
        self.relaciones.update({elemento:[]})

    def relacionar(self, origen, destino):
        self.relaciones[origen].append(destino)

    def eliminar(self, elemento):
        del self.relaciones[elemento]
        for i in self.relaciones:
            if self.relaciones[i] == [elemento]:
                del self.relaciones[i][0]

    def actualizar(self, relaciones):
        for relacion in relaciones:
            origen, destino = relacion[0], relacion[2]
            if origen in self.relaciones:
                if not(destino in self.relaciones):
                    self.agregar(destino)
            else:
                self.agregar(origen)

            self.relaciones[origen].append(destino)



def recorrer(grafo, elementoInicial, elim_bloqueo, elementosRecorridos = []):
    if elementoInicial in elementosRecorridos:
        print "\n Hay bloqueo. Se esta eliminando un proceso ..."
        grafo.estado = "Hay bloqueo"
        time.sleep(1)

        if elim_bloqueo:
            grafo.eliminar(elementoInicial)
            grafo.estado = "Sin bloqueo"
        return

    #print elementoInicial, "->",
    elementosRecorridos.append(elementoInicial)
    try:
        for vecino in grafo.relaciones[elementoInicial]:
            recorrer(grafo, vecino, elim_bloqueo, elementosRecorridos)
    except KeyError:
        pass



# PARAMETROS LOCALES

recursoS = "S"
recursoR = "R"
recursoT = "T"
procesoA = "A"
procesoB = "B"
procesoC = "C"

grafo = Grafo()
grafo.agregar(recursoS)
grafo.agregar(recursoR)
grafo.agregar(recursoT)
grafo.agregar(procesoA)
grafo.agregar(procesoB)
grafo.agregar(procesoC)

grafo.relacionar(recursoT, procesoC)
grafo.relacionar(procesoC, recursoS)
grafo.relacionar(recursoS, procesoA)
grafo.relacionar(procesoA, recursoR)
grafo.relacionar(recursoR, procesoB)

# PREPARAR PUERTOS PARA ESCUCHAR PETICIONES:
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 3000))
s.listen(10)

# CONEXION PARA CADA CLIENTE:
def connection(sc, address):
    data = sc.recv(1024)
    while True:
        if data > 0:
            if type(data) == type("a"):
                print "Mensaje recibido: ", data
                data = data.split(";")
                intervalo_act = int(data[0])
                data.remove(data[0])
                nuevas_relaciones = data
                grafo.actualizar(nuevas_relaciones)
                print "Intervalo para actualizar: ", intervalo_act
                print "Nuevas relaciones para agregar: ", nuevas_relaciones
            #print "------------------------------------------"
            sc.send(grafo.estado)
        time.sleep(intervalo_act)

def mostrarGrafo(grafo, tiempo):
    while True:
        time.sleep(tiempo)
        print "------------------------------------------"
        print "GRAFICO DE RECURSOS"
        print "------------------------------------------"
        recorrer(grafo, list(grafo.relaciones)[0], True, [])
        print grafo
        print "\n------------------------------------------"
crearGrafo = True

while 1:
    if crearGrafo:
        thread.start_new_thread(mostrarGrafo, (grafo, 10))
        crearGrafo = False
    print "Esperando conexiones..."

    sc, addr = s.accept()
    print "------------------------------------------"
    print "Recibí una conexion de: ", addr[0], ":", addr[1]
    thread.start_new_thread(connection, (sc, addr))

ss.close()
s.close()
