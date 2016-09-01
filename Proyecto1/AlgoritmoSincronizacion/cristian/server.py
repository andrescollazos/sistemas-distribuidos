#!/usr/bin/env python
from socket import AF_INET, SOCK_DGRAM
import sys
import socket
import struct, time

# HORA DESDE SERVIDOR NTP - ACTUANDO COMO CLIENTE
host = "pool.ntp.org"
address = (host, 123)
msg = '\x1b' + 47 * '\0'
time1970 = 2208988800L

client = socket.socket(AF_INET, SOCK_DGRAM)
tiempo_init = time.time()
client.sendto(msg, address)
msg, address = client.recvfrom( 1024)
tiempo_fin = time.time()

t = struct.unpack( "!12I", msg )[10] # CONVERTIR A HORA
t -= time1970
t = int(t)
#print "SE DEMORO {0} \n {1}".format((tiempo_fin - tiempo_init), time.ctime(t).replace(" ", " "))

# ESPERAR SOLICITUDES DE CLIENTES - ACTUANDO COMO SERVIDOR
TCP_IP = '127.0.0.1'
TCP_PORT = 6021

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
print 'Connection address: {0}'.format(addr)

while 1:
    data = conn.recv(20)
    if len(data) > 0:
        if data == "1":
            data = str(t)
    if not data : break
    conn.send(data)
conn.close()
