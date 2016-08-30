#!/usr/bin/env python
from socket import AF_INET, SOCK_DGRAM
import sys
import socket
import struct, time

host = "pool.ntp.org"

address = (host, 123)
msg = '\x1b' + 47 * '\0'

time1970 = 2208988800L

client = socket.socket(AF_INET, SOCK_DGRAM)
tiempo_init = time.time()
client.sendto(msg, address)
msg, address = client.recvfrom( 1024)
tiempo_fin = time.time()

t = struct.unpack( "!12I", msg )[10]
t -= time1970
print "SE DEMORO {0} \n {1}".format((tiempo_fin - tiempo_init), time.ctime(t).replace(" ", " "))
