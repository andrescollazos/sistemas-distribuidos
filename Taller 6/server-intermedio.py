# coding=utf-8

# Librerias
#Se importa el módulo ServerProxy de xmlrpclib.
from xmlrpclib import ServerProxy
from SimpleXMLRPCServer import SimpleXMLRPCServer
# ACTUANDO COMO SERVIDOR ANTE CLIENTE
s = SimpleXMLRPCServer(("", 5005))

def operacion(a, b, op):
    if op == '+':
        # ACTUANDO COMO CLIENTE ANTE LOS SERVIDORES DE OPERACIONES:
        S = ServerProxy('http://localhost:6000')
        return S.suma(a, b)
        #return a + b
    elif op == '-':
        S = ServerProxy('http://localhost:7000')
        return S.resta(a, b)
    elif op == '*':
        S = ServerProxy('http://localhost:8000')
        return S.multiplicacion(a, b)
    elif op == '/' and b != 0:
        S = ServerProxy('http://localhost:9000')
        return S.division(a, b)
    elif op == '^':
        S = ServerProxy('http://localhost:10000')
        return S.potenciacion(a, b)
    elif op == 'log' and a > 0 and b > 0:
        S = ServerProxy('http://localhost:11000')
        return S.logaritmo(a, b)
    elif op == 'sqr' and a > 0:
        S = ServerProxy('http://localhost:12000')
        return S.radicacion(a, b)
    return "ERROR: OPERACION NO VALIDA!!"

#se registra la función
s.register_function(operacion)

#se inicia el servidor
s.serve_forever()
