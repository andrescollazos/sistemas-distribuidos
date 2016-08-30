# coding=utf-8

# Librerias
from SimpleXMLRPCServer import SimpleXMLRPCServer
s = SimpleXMLRPCServer(("", 12000))

def radicacion(a, b):
    return a ** (1.0/b)

#se registra la función
s.register_function(radicacion)

#se inicia el servidor
s.serve_forever()
