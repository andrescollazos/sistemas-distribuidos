#!/usr/bin/env python
from socket import AF_INET, SOCK_DGRAM
import sys
import socket
import struct, time
import thread
from claseReloj import Reloj

# HORA DESDE SERVIDOR NTP - ACTUANDO COMO CLIENTE
client = socket.socket(AF_INET, SOCK_DGRAM)
tiempo_init = time.time()
client.sendto('\x1b' + 47 * '\0', ("pool.ntp.org", 123))
msg, address = client.recvfrom(1024)
tiempo_fin = time.time()

t = struct.unpack("!12I", msg)[10] # CONVERTIR A HORA
t = int(t - 2208988800L)
horaI = time.ctime(t).replace(" ", " ")
print "Hora recibida desde el servidor NTP: ", horaI
print "Latencia (ms): ", int(1000*(tiempo_fin - tiempo_init))

# AJUSTAR RELOJ LOCAL DEL SERVER
relojSys = Reloj()
crearReloj = True
relojSys.setHora(int(horaI[11]+horaI[12]), int(horaI[14]+horaI[15]), int(horaI[17]+horaI[18]), int(1000*(tiempo_fin - tiempo_init)))

# PREPARAR LOS PUERTOS PARA ESCUCHAR LAS PETICIONES
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 3000))
s.listen(10)

def connection(sc, address, reloj):
    data = sc.recv(1024)
    while True:
        if data > 0:
            print "La hora del servidores es: ", reloj.retHora()
            respuesta = reloj.retHora()

            sc.send(respuesta)
        time.sleep(int(data))
'''
    if data == "1":
        print "La hora del servidores es: ", reloj.retHora()
        respuesta = reloj.retHora()

        sc.send(respuesta)
'''
while 1:
    if crearReloj:
        thread.start_new_thread(relojSys.tick,())
        crearReloj = False
    print "A la espera de las conexiones... "

    sc, addr = s.accept()
    print "recibida conexion de la IP: " + str(addr[0]) + " puerto: " + str(addr[1])
    thread.start_new_thread(connection,(sc,addr, relojSys))

sc.close()
s.close()
