# coding=utf-8

# Librerias
from SimpleXMLRPCServer import SimpleXMLRPCServer
s = SimpleXMLRPCServer(("", 10000))

def potenciacion(a, b):
    return a ** b

#se registra la función
s.register_function(potenciacion)

#se inicia el servidor
s.serve_forever()
