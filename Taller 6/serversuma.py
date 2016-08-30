# coding=utf-8

# Librerias
from SimpleXMLRPCServer import SimpleXMLRPCServer
s = SimpleXMLRPCServer(("", 6000))

def suma(a, b):
    return a + b

#se registra la función
s.register_function(suma)

#se inicia el servidor
s.serve_forever()
