
#!/usr/bin/env python

import socket
import math


TCP_IP = '127.0.0.1'
TCP_PORT = 5014

while 1:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)

    conn, addr = s.accept()
    print 'Connection address: {0}'.format(addr)

    while 1:
        data = conn.recv(20)
        op = []
        #op, cont = ["","",""], 0
        if len(data) > 0:
            op = data.split(" ")
            #print "num1 {0}, num2 {1}, op {2}".format(op[0], op[1], op[2])

            # RETORNA LOS PUERTOS DE LOS GRUPOS QUE REALIZAN LA OPERACION
            if op[2] == '+':
                resp = "5016:5017:5018"
            elif op[2] == '-':
                resp = "5016"
            elif op[2] == '*':
                resp = "5017"
            elif op[2] == '/':
                resp = "5016"
            elif op[2] == '^':
                resp = "5018"
            elif op[2] == 'sqr':
                resp = "5019"
            elif op[2] == 'log':
                resp = "5019"
            #print "La respuesta es: {0}".format(resp)
            data = resp

        if not data: break
        conn.send(data)  # echo
    conn.close()
