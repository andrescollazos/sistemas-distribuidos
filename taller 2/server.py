#!/usr/bin/env python

import socket
import math

TCP_IP = '192.168.8.61'
TCP_PORT = 6015
nomarchivo = "llamoalajuventud.txt"
archivo = open(nomarchivo, "r")
contenido = archivo.read()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
print 'Connection address: {0}'.format(addr)

contador = 0
while 1:
    data = conn.recv(20)
    if len(data) > 0:
        for i in contenido:
            if data == i or data.upper() == i:
                contador += 1
        data = "En el archivos "+nomarchivo+" la vocal "+data+" se repite "+str(contador)+" veces.!"
        print data

    if not data: break
    conn.send(data)  # echo
conn.close()
