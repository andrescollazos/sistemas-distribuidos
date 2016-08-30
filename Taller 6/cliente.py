# coding=utf-8

#Se importa el módulo ServerProxy de xmlrpclib.
from xmlrpclib import ServerProxy
#Se conecta al equipo por el puerto 5005
s = ServerProxy('http://localhost:5005')

salir = False
while not salir:
    num1 = input("Digite un numero: ")
    num2 = input("Digite otro numero: ")
    op1 = raw_input("Operacion? (+)(-)(*)(/)(^)(sqr)(log): ")
    try:
        print "\nLa respuesta es: ", s.operacion(num1, num2, op1)
    except OverflowError:
        print "\nLos numeros ingresados son muy grandes! Exceden capacidad!"

    salir = raw_input("\n\nDesea continuar? (Y/N): ")

    if salir == "N" or salir == "n":
        salir = True
    else:
        salir = False
