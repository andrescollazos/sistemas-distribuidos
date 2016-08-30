# coding=utf-8

# Librerias
from SimpleXMLRPCServer import SimpleXMLRPCServer
s = SimpleXMLRPCServer(("", 9000))

def division(a, b):
    return a / b

#se registra la función
s.register_function(division)

#se inicia el servidor
s.serve_forever()
