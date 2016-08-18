#!/usr/bin/env python

import socket


TCP_IP = '192.168.8.61'
TCP_PORT = 6015
while 1:
    MESSAGE = raw_input("Digite una vocal: ")
    if MESSAGE=='a' or MESSAGE=='e' or MESSAGE=='i' or MESSAGE=='o' or MESSAGE=='u':
        break
    else:
        print "No es una vocal"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(MESSAGE)
data = s.recv(1024)
s.close()

print data
