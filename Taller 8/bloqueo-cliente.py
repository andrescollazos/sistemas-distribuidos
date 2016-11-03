# -*- coding: utf-8 -*

import socket
import time
import thread
import sys

intervalo = "10" # CADA CUANTOS SEGUNDOS PIDE ACTUALIZACIÓN AL SERVER

# CONEXION A SERVIDOR
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.connect(('localhost', 3000))

def main(argv):
    mensaje = argv[1]
    resp_ant = 0
    #print mensaje

    print "------------------------------------------"
    print "Enviare un mensaje al server!"
    print "------------------------------------------"
    while True:
        s.send(mensaje)

        respuesta = s.recv(1024)
        if respuesta != resp_ant:
            print "------------------------------------------"
            print "SERVER: ", respuesta
            print "------------------------------------------"
            resp_ant = respuesta
    s.close()

main(sys.argv)
