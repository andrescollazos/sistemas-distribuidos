import sys
import socket
#import struct, time
import time
import thread
import threading

TCP_IP = 'localhost'
TCP_PORT = int(sys.argv[1])#11000
BUFFER_SIZE = 2048
cambiarCoordinador = False
contadorProcesos = 0
#procesosMasGrandes = 0
# Proceso : [Direccion, puerto, prioridad, estado, esCoordinador?, esElegibleComoCordinador?]
procesos =[
			['localhost', 6111, '2', 'active', False, 'ne'],
			['localhost', 6222, '4', 'active', False, 'ne'],
			['localhost', 6333, '6', 'inactive', True, 'ne']
			]
'''
			['localhost', 14000, '1', 'active', False, 'ne'],
			['localhost', 15000, '3', 'active', False, 'ne'],
			['localhost', 16000, '5', 'active', False, 'ne'],
			['localhost', 17000, '7', 'active', False, 'ne'],
			['localhost', 18000, '8', 'inactive', True, 'ne'],
		  ]
'''
# ELIMINARSE DE LA LISTA DE PROCESOS:
estado = ''
prioridad = 0
soyCoordinador = False
for i in procesos:
	if TCP_PORT in i:
		estado = i[3]
		prioridad = i[2]
		soyCoordinador = i[4]
		procesos.remove(i)

#SocketServer.ThreadingTCPServer.allow_reuse_address = True
#s = socket.socket	(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(10)

# MENSAJE TIPO E:
def escogerCoordinador(IP, Puerto):
	global cambiarCoordinador
	global contadorProcesos
	s = socket.socket()
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.connect((IP, Puerto))
	print "Enviare mensaje \"E\" a : ", IP, ":", Puerto
	s.send("E")
	time.sleep(1)
	ok = s.recv(BUFFER_SIZE)
	time.sleep(1)

	if ok == 'OK':
		print "Recibi mensaje \"OK\", ya no soy elegible como coordinador"
		cambiarCoordinador = False
	elif ok == '-1':
		print "ME llego un mensaje -1"
		contadorProcesos = contadorProcesos + 1
	#print ok
	#Hour = Hour+int(HorRec)

	s.close()

def peticionCoordinador(IP, Puerto):
	s = socket.socket()
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.connect((IP, Puerto))
	print "Enviare peticion al coordinador: ", IP, ":", Puerto
	s.send("1")
	time.sleep(1)
	activo = s.recv(BUFFER_SIZE)
	time.sleep(1)
	print "Estoy ", activo
	s.close()

	if activo == 'inactive':
		return "Cambio"
	else:
		return "No Cambio"

def connection(sc, addr):
	#global Segundos, Minutos, Hora
	global cambiarCoordinador
	Pregunta=sc.recv(BUFFER_SIZE)
	if Pregunta == "E":
		if estado == 'active':
			print "ESTOY ACTIVO -> Enviare respuesta \"OK\" a ", addr[0], ":", addr[1]
			#HoraEnviada = (Hora*3600)+(Minutos*60)+Segundos
			cambiarCoordinador = True
			sc.send("OK")
		else:
			print "ESTOY INACTIVO -> Enviare respuesta -1 a ", addr[0], ":", addr[1]
			sc.send(str(-1))

	elif Pregunta == "1":
		print "Enviare mi estado a ", addr[0], ":", addr[1]
		sc.send(estado)


def Cliente():
	while True:
		sc, addr = s.accept()
		thread.start_new_thread(connection,(sc,addr))

threads = list()

t = threading.Thread(target=Cliente)
threads.append(t)
t.start()

# Para llevar a cabo la simulacion del proceso: el proceso 2, el cual tiene el
# asociado el puerto 31000, identifico
empezar = True
value = False
while True:
	time.sleep(10)

	if TCP_PORT == 6111 and empezar: # Proceso 2
		for i in procesos:
			if True in i: # Buscar coordinador
				cambiar = peticionCoordinador(i[0], i[1])
				if cambiar == "Cambio":
					print "Hay que cambiar de coordinador!"
					cambiarCoordinador = True
				else:
					print "El coordinador resolvio mi peticion"
		empezar = False

	if cambiarCoordinador:
		procesosMasGrandes = 0
		for i in procesos:#range(len(procesos)):
			if prioridad < i[2]:
				procesosMasGrandes = procesosMasGrandes + 1
				thread.start_new_thread(escogerCoordinador,(i[0],i[1]))

				#print "CAMBIAR COORDINADOR: ", cambiarCoordinador
		value = True
	#print "TCP_PORT:", TCP_PORT, "contadorProcesos= ", contadorProcesos
	if value:
		if contadorProcesos == procesosMasGrandes:
			print "Soy el nuevo coordinador! ... :)"
