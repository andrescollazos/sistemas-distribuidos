# coding=utf-8

# Librerias
from SimpleXMLRPCServer import SimpleXMLRPCServer
s = SimpleXMLRPCServer(("", 7000))

def resta(a, b):
    return a - b

#se registra la función
s.register_function(resta)

#se inicia el servidor
s.serve_forever()
