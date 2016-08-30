#!/usr/bin/env python
# RESTA

import socket
import math


TCP_IP = '127.0.0.1'
TCP_PORT = 8000

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
            print "num1 {0}, num2 {1}, -".format(op[0], op[1])

            data = str(float(op[0])-float(op[1]))

        if not data: break
        conn.send(data)  # echo
    conn.close()
