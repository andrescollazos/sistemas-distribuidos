#!/usr/bin/env python

import socket
import math
import thread

TCP_IP = '127.0.0.1'
TCP_PORT = 5020

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)



bandera = 0

def escuchar():
    pass

while 1:
    conn, addr = s.accept()
    print 'Connection address: {0}'.format(addr)

    data = conn.recv(1024)
    if(data == "solicitud"):
        print "He recibido una solicitud"
        if bandera == 0:
            data = "otorgado"
            bandera = 1
        else:
            data = "denegado"

    if not data:
        break
    else:
        conn.send(data)  # echo

    data = conn.recv(1024)
    if data == "liberar":
        print "Se libero el recurso"
        bandera = 0
    conn.close()
