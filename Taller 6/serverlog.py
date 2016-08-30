# coding=utf-8

# Librerias
from SimpleXMLRPCServer import SimpleXMLRPCServer
from math import log
#Se asocia a un puerto en este caso 6000
s = SimpleXMLRPCServer(("", 11000))

def logaritmo(a, b):
    return log(a, b)

#se registra la función
s.register_function(logaritmo)

#se inicia el servidor
s.serve_forever()
