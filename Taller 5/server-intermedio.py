#!/usr/bin/env python

import socket
import math


TCP_IP = '127.0.0.1'
TCP_PORT = 5555
#TCP_PORT_S = 5556

while 1:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)

    conn, addr = s.accept()
    print 'Connection address: {0}'.format(addr)

    while 1:
        data = conn.recv(20)
        op = []
        if len(data) > 0:
            op = data.split(" ")
            # ESCOGER SERVIDOR INDICADO (PUERTO POR OPERACION):
            if op[2] == '+':
                TCP_PORT_S = 7000
            elif op[2] == '-':
                TCP_PORT_S = 8000
            elif op[2] == '*':
                TCP_PORT_S = 9000
            elif op[2] == '/':
                TCP_PORT_S = 10000
            elif op[2] == '^':
                TCP_PORT_S = 11000
            elif op[2] == 'sqr':
                TCP_PORT_S = 12000
            elif op[2] == 'log':
                TCP_PORT_S = 13000

            # ACTUANDO COMO CLIENTE HACIA EL SERVIDOR server.py
            MESSAGE = op[0]+" "+op[1] # MANDAR NUMERO 1 Y NUMERO 2
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((TCP_IP, TCP_PORT_S))
            s.send(MESSAGE)
            data = s.recv(1024)
            s.close()

        if not data: break
        conn.send(data)  # RESPONDIENDO COMO SERVIDOR HACIA CLIENTE
    conn.close()
