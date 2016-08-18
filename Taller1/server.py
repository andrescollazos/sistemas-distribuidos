#!/usr/bin/env python

import socket
import math


TCP_IP = '127.0.0.1'
TCP_PORT = 5015

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
print 'Connection address: {0}'.format(addr)

while 1:
    data = conn.recv(20)
    op, cont = ["","",""], 0
    if len(data) > 0:
        for i in data:
            if i != ' ':
                op[cont] += i
            else:
                cont += 1
        print "num1 {0}, num2 {1}, op {2}".format(op[0], op[1], op[2])

        if op[2] == '+':
            resp = int(op[0]) + int(op[1])
            resp = str(resp)
        elif op[2] == '-':
            resp = int(op[0]) - int(op[1])
            resp = str(resp)
        elif op[2] == '*':
            resp = int(op[0]) * int(op[1])
            resp = str(resp)
        elif op[2] == '/':
            resp = int(op[0]) / int(op[1])
            resp = str(resp)
        elif op[2] == '^':
            resp = int(op[0]) ** int(op[1])
            resp = str(resp)
        elif op[2] == 'sqr':
            resp = int(op[0])**(1.0/int(op[1]))
            resp = str(resp)
        elif op[2] == 'log':
            resp = math.log(int(op[0]), int(op[1]))
            resp = str(resp)
        #print "La respuesta es: {0}".format(resp)
        data = resp

    if not data: break
    conn.send(data)  # echo
conn.close()
