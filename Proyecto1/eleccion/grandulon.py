import sys
import socket
#import struct, time
import time
import thread
import threading

TCP_IP = 'localhost'
TCP_PORT = int(sys.argv[1])#11000
BUFFER_SIZE = 2048

procesos =[
			['localhost', 31000, 'active', False],
			['localhost', 32000, 'active', False],
			['localhost', 33000, 'active', False]
			]
'''
			['localhost', 14000, 'active', False],
			['localhost', 15000, 'active', False],
			['localhost', 16000, 'active', False],
			['localhost', 17000, 'active', False],
			['localhost', 18000, 'inactive', True],
		  ]
'''
# ELIMINARSE DE LA LISTA DE PROCESOS:
for i in procesos:
	if TCP_PORT in i:
		procesos.remove(i)
#SocketServer.ThreadingTCPServer.allow_reuse_address = True
#s = socket.socket	(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(10)

# MENSAJE TIPO E:
def escogerCoordinador(IP,Puerto):
		#global Hour
		#print "IP: ", IP, " Puerto: ", Puerto
		#time.sleep(5)
		s = socket.socket()
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.connect((IP, Puerto))
		print "Enviare mensaje \"E\" a : ", IP, ":", Puerto
		s.send("E")
		time.sleep(1)
		ok = s.recv(BUFFER_SIZE)
		time.sleep(1)
		print ok
		#Hour = Hour+int(HorRec)

		s.close()

def connection(sc, addr):
	#global Segundos, Minutos, Hora

	Pregunta=sc.recv(BUFFER_SIZE)
	if Pregunta == "E":
		print "Enviare respuesta \"OK\" a ", addr[0], ":", addr[1]
		#HoraEnviada = (Hora*3600)+(Minutos*60)+Segundos
		sc.send("OK")


def Cliente():
	while True:
		sc, addr = s.accept()
		thread.start_new_thread(connection,(sc,addr))

threads = list()

t = threading.Thread(target=Cliente)
threads.append(t)
t.start()

while True:
	time.sleep(10)

	if TCP_PORT == 31000:
		for i in range(len(procesos)):
			thread.start_new_thread(escogerCoordinador,(procesos[i][0],procesos[i][1]))

	#Hour = Hour + ( ( Hora * 3600 ) + ( Minutos * 60 ) + Segundos )
	#Hour = Hour / ( len(Clientes) + 1 )
	#Hora = Hour/3600
	#Hour = Hour - (Hora*3600)
	#Minutos = Hour/60
	#Hour = 0

#if __name__ == '__main__':
#	main()
