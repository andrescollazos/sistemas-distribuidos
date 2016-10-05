#!/usr/bin/env python

import socket
import time
import thread

TCP_IP = '127.0.0.1'
TCP_PORT = 5020

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

while 1:

    MESSAGE = "solicitud"
    s.send(MESSAGE)

    data = s.recv(1024)

    print "Me mandaron " + data

    if data == "otorgado":
        print "entrando en seccion critica"
        time.sleep(5)
        MESSAGE = "liberar"
        s.send(MESSAGE)
    else:
        print "alguien mas esta en seccion critica"
        s.send(MESSAGE)
        MESSAGE = "solicitud"

s.send(MESSAGE)
s.close()

print "\nRespuesta: {0}".format(data)
