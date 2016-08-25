
#!/usr/bin/env python

import socket


TCP_IP = '127.0.0.1'
TCP_PORT = 5014
while 1:
    num1 = raw_input("Digite un numero: ")
    num2 = raw_input("Digite otro numero: ")
    op1 = raw_input("Operacion? (+)(-)(*)(/)(^)(sqr)(log): ")
    MESSAGE = num1+" "+num2+" "+op1

    #MESSAGE = "Hello, World!"

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send(MESSAGE)
    data = s.recv(1024)
    s.close()

    print "\nPUERTOS DISPONIBLES: {0}".format(data)

    puertos = data.split(":")
    for i in puertos:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, int(i)))
        s.send(MESSAGE)
        data = s.recv(1024)
        s.close()

        print "RESPUETA RECIBIDA DE {0}:{1}\n{2} {3} {4} = {5}".format(TCP_IP, int(i), op1, num1, num2, data)

    print "--------------------------------"
