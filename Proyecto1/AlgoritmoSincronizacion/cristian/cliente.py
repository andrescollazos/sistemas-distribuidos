#!/usr/bin/env python

import socket
import time


TCP_IP = '127.0.0.1'
TCP_PORT = 6021

#num1 = raw_input("Digite un numero: ")
#num2 = raw_input("Digite otro numero: ")
#op1 = raw_input("Operacion? (+)(-)(*)(/)(^)(sqr)(log): ")
MESSAGE = "1" #num1+" "+num2+" "+op1

#MESSAGE = "Hello, World!"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(MESSAGE)
data = s.recv(1024)
s.close()

data = int(data)
print "\nLa Hora es: {0}".format(time.ctime(data).replace(" ", " "))
