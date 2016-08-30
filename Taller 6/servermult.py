# coding=utf-8

# Librerias
from SimpleXMLRPCServer import SimpleXMLRPCServer
s = SimpleXMLRPCServer(("", 8000))

def multiplicacion(a, b):
    return a * b

#se registra la función
s.register_function(multiplicacion)

#se inicia el servidor
s.serve_forever()
