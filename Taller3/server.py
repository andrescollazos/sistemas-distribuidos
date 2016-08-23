# coding=utf-8

# Librerias
from SimpleXMLRPCServer import SimpleXMLRPCServer
from math import log
#Se asocia a un puerto en este caso 5005
s = SimpleXMLRPCServer(("", 5005))
#La función que toma x y devuelve el doble de x.
def operacion(a, b, op):
    if op == '+':
        return a + b
    elif op == '-':
        return a - b
    elif op == '*':
        return a * b
    elif op == '/' and b != 0:
        return a*1.0 / b
    elif op == '^':
        return a ** b
    elif op == 'log' and a > 0 and b > 0:
        return log(a, b)
    elif op == 'sqr':
        return a**(1.0/b)
    return "ERROR: OPERACION NO VALIDA!!"

#se registra la función
s.register_function(operacion)

#se inicia el servidor
s.serve_forever()
