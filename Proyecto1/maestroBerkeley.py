#!/usr/bin/env python
from socket import AF_INET, SOCK_DGRAM
import sys
import socket
import struct, time
import thread
from claseReloj import *

# AJUSTAR RELOJ LOCAL DEL SISTEMA
relojSys = Reloj()
crearReloj = True
l = time.localtime()
relojSys.setHora(l.tm_hour, l.tm_min, l.tm_sec, 0)

# PREPARAR LOS PUERTOS PARA ESCUCHAR LAS PETICIONES
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 3000))
s.listen(10)

class Maestro():
    def __init__(self):
        self.conectados = []
        self.listaDesface = []

    def mostrarTiempo(self):
        while 1:
            time.sleep(10)
            print "##### ------> Lista de conectados: "
            for i in self.conectados:
                print "* ", i[1], " - ", i[0]

    def calcDesface(self, relojSys):
        sumDesface, cont = 0, 0
        #print "antes: ", len(self.conectados)

        for i in self.conectados:
            relojTemp = Reloj(i[1])
            #print "Desface con ", i[0], " : ", relojSys.desface(relojTemp)
            sumDesface = sumDesface + relojSys.desface(relojTemp)
            cont = cont + 1
        promedio = (sumDesface*1.0) / (cont + 1)
        return promedio

def mostrarHoraSys(reloj, sec):
    while 1:
        print "##### ------> Hora local del maestro: ", reloj.retHora()
        time.sleep(sec)

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
            #print "hora sistema:", reloj.retHora()
            print str(address[0]) + ":" + str(address[1]) + ": ", data
            if not ((address, data) in maestro.conectados):
                #print "conect - OK"
                maestro.conectados.append((address, data))

            promedio = maestro.calcDesface(reloj)
            for i in maestro.conectados:
                if address == i[0]:
                    relojTemp = Reloj(data)
                    desfacei = relojSys.desface(relojTemp)
                    desfacei = convertSectoHourMinSecMsec(promedio - desfacei)
                    respuestaDesface = str(desfacei[0]) +":"+ str(desfacei[1]) +":"+ str(desfacei[2]) +":"+ str(desfacei[3]) +":"+ str(desfacei[4])
                    sc.send(respuestaDesface)
                    print respuesta

            desfaceSys = convertSectoHourMinSecMsec(promedio)
            relojSys.ajustarHora(desfaceSys[0]*desfaceSys[4], desfaceSys[1]*desfaceSys[4], desfaceSys[2]*desfaceSys[4], desfaceSys[3]*desfaceSys[4])
            print "Mi nueva hora es: ", relojSys.retHora()

print "A la espera de las conexiones... "
maestro = Maestro()
while 1:
    if crearReloj:
        thread.start_new_thread(relojSys.tick,()) # INICIAR EL RELOJ
        thread.start_new_thread(mostrarHoraSys,(relojSys, 10)) # MOSTRAR HORA CADA n SEGUNDOS
        #thread.start_new_thread(maestro.mostrarTiempo,()) # MOSTRAR HORA CADA n SEGUNDOS
        crearReloj = False
    #print "A la espera de las conexiones... "

    sc, addr = s.accept()
    #print "recibida conexion de la IP: " + str(addr[0]) + " puerto: " + str(addr[1])
    thread.start_new_thread(connection,(sc,addr, relojSys))
    #maestro.conectados.append(addr)
    #maestro.calcDesface(relojSys)

sc.close()
s.close()
