#!/usr/bin/env python
# coding=utf-8

import socket
import time
import thread
from claseReloj import Reloj
import sys
import random

# ------------------------------------------------------------------------------
#                CLASE PARA EL MANEJO DE LAS PAGINAS DEL NODO
# ------------------------------------------------------------------------------
class Paginas():
    def __init__(self, init = []):
        self.paginas = []      # Se cuenta con una lista de paginas -> [101, 102, 103, ...]
        self.directorio = ""   # Se tiene un directorio de trabajo
        self.estadoEscribir = 0
        self.estadoLeer = 0

        if len(init) > 0:     # Se puede inicializar el objeto al crearlo
            self.directorio = init[0]
            self.paginas = init[1:]

    # Metodo para imprimir el objeto al ser llamado por la funcion print -> print MiPagina
    def __str__(self):
        return "Directorio de Trabajo: {0} \n Lista de Paginas: {1}".format(self.directorio, str(self.paginas))

    # Agregar una pagina
    def registrarPag(self, pag):
        self.paginas.append(pag)

    # Modificar una variable en la pagina, se recibe una pagina, la posición y un valor
    # Ejemplo:
    # Se cuenta con una pagina '101' de esta manera:
    # 0 0 0 0
    # 0 0 0 0
    # 0 0 0 0
    # Y se quiere modificar el valor de la primera posición (0, 0) y el valor (2, 3)
    # Input: escribirPag('101', [0, 0], 'X') y escribirPag('101', [2, 3], 'y')
    # Output:
    # X 0 0 0
    # 0 0 0 0
    # 0 0 0 y
    def escribirPag(self, pag, pos, value):
        # Se verificar que la posición que se quiere modificar si se encuentra en la pagina
        if pos[0] >= 0 and pos[0] < 10 and pos[1] >= 0 and pos[1] < 10:
            if pag in self.paginas: # Se verifica que la pagina este en el directorio de trabajo
                # Se utiliza la ruta para llegar al archivo: "nombre_directorio/numero_pagina"
                arch = open(self.directorio+"/"+pag, "r+") # r+ -> Modo lectura y escritura
                final = arch.tell() # Conocer el final del archivo

                # 2 * (pos[0]*10 + pos[1])
                # 2         ->  Ya que se cuenta con espacios, se multipla la posición
                # pos[0]*10 ->  Un archivo a pesar de los saltos de linea, se lee como si fuera
                #               una sola linea, entonces es necesario calcular como si se tratara de un vector
                # pos[1]    ->  Ubicarse en la columna
                arch.seek(2*(pos[0]*10 + pos[1]))
                arch.write(str(value))
            else:
                print "Error: ¡La pagina solicitada no se encuentra en el directorio!"
        else:
            print "Error: ¡La posición de la pagina no es valida!"

    # Este metodo simulara la actualización de las paginas, cada cierto tiempo,
    # Se realizará una modificación con un valor aleatoreo a una pagina
    # seleccionada aleatoreamente
    def actualizarPag(self, socket, tiempo = 3):
        tiempo_inicial = tiempo
        while True:
            time.sleep(int(tiempo))
            socket.send("E")
            autorizacion = socket.recv(1024)
            print "Recibí respuesta: ", autorizacion
            if autorizacion == '1':
                tiempo = tiempo_inicial
                #self.estadoEscribir = 1 # EL NODO VA A ESCRIBIR EN UNA PAGINA
                valor = random.randrange(0, 10)
                pos = [random.randrange(0, 10), random.randrange(0, 10)]
                pagina = self.paginas[random.randrange(0, len(self.paginas))]
                print "Escribiendo el valor {3} en la pagina {0} en la posición ({1}, {2})".format(pagina, pos[0], pos[1], valor)
                self.escribirPag(pagina, pos, valor)
                mensaje = "E-" + pagina + "-" + str(pos[0]) + "," + str(pos[1]) + "-" + str(valor)
                socket.send(mensaje)
            else:
                tiempo = 0.05

    def leerPag(self, socket, tiempo = 10):
        tiempo_inicial = tiempo
        while True:
            time.sleep(int(tiempo))
            socket.send("L")
            autorizacion = socket.recv(1024)
            print "Recibí respuesta: ", autorizacion

            if autorizacion == '1':
                tiempo = tiempo_inicial
                #self.estadoLeer = 1
                pos = [random.randrange(0, 10), random.randrange(0, 10)]
                pagina = self.paginas[random.randrange(0, len(self.paginas))]
                arch = open(self.directorio+"/"+pagina, "r+")
                arch.seek(2*(pos[0]*10 + pos[1]))
                valor = arch.read(1)
                print "Leyendo el valor de en la pagina {0} en la posición ({1}, {2}): {3}".format(pagina, pos[0], pos[1], valor)
                #self.estadoLeer = 0
                mensaje = "L-" + pagina + "-" + str(pos[0]) + "," + str(pos[1]) + "-" + str(valor)
                socket.send(mensaje)
            else:
                tiempo = 0.05

# ------------------------------------------------------------------------------
#                     AJUSTES DE SINCRONIZACIÓN DE RELOJ
# ------------------------------------------------------------------------------

intervalo = "5" # CADA CUANTOS SEGUNDOS PIDE AL SERVIDOR LA HORA

# CONEXION A SERVIDOR
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.connect(('localhost', int(sys.argv[1])))
s.send(sys.argv[2])

# AJUSTAR RELOJ LOCAL DEL SISTEMA
relojSys = Reloj()
iniciarProceso = True
l = time.localtime()
relojSys.setHora(l.tm_hour, l.tm_min, l.tm_sec)

#print "La hora del sistema antes de llamar al servidor: ", relojSys.mostrarHora()

continuar = True

paginas_nodo = Paginas(['1', '100'])

while continuar:
    if iniciarProceso:
        #thread.start_new_thread(relojSys.tick,())
        thread.start_new_thread(paginas_nodo.actualizarPag,(s, 5))
        thread.start_new_thread(paginas_nodo.leerPag,(s, 17))
        iniciarProceso = False
    #print "-------------------------------------------------------------"
    #print "La hora del sistema antes de llamar al servidor: ", relojSys.mostrarHora()

    #s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #s.connect(('localhost', sys.argv[1]))
    #if paginas_nodo.estadoEscribir:
    #    mensaje =
    #tiempo_init = time.time()

    #time.sleep(1)
    #s.send(sys.argv[2]) # CADA CUANTOS SEGUNDOS PIDE LA HORA
    #horaRecibida = s.recv(1024)
    #tiempo_fin = time.time()

    #print "La hora del sistema despues de llamar al servidor: ", relojSys.mostrarHora()
    #print "La latencia cliente-servidor por la red (seg.): ", int(1000*(tiempo_fin - tiempo_init))
    #print "La hora recibida del servidor: ", horaRecibida

    #### MODIFICAR HORA DEL CLIENTE
    #newHour = int(horaRecibida[0]+horaRecibida[1])
    #newMin = int(horaRecibida[3]+horaRecibida[4])
    #newSec = int(horaRecibida[6]+horaRecibida[7])
    #newMil = int(horaRecibida[9]+horaRecibida[10]+horaRecibida[11])
    #relojSys.setHora(newHour, newMin, newSec, newMil)
    #print horaRecibida
    #print "\n La nueva hora del cliente: ", relojSys.mostrarHora()


    resp = 'y' #raw_input("Desea ajustar nuevamente la hora? (y/n): ")
    if resp == 'Y' or resp == 'y':
        continuar = True
    else:
        continuar = False
#s.close()
