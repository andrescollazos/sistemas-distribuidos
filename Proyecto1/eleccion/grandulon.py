from socket import AF_INET, SOCK_DGRAM
import time
import socket
import thread

global procesos
procesos = []

class Proceso():
    global procesos

    def __init__(self, nom, prioridad, status, address, coordinador=False):
        self.nom = nom
        self.prioridad = prioridad
        self.status = status
        self.coordinador = coordinador
        self.address = address
        #self.procesos = []

    def mostrarProceso(self):
        return self.nom + " prioridad: "+str(self.prioridad)+" s:"+self.status+ " - "+str(self.address)

    def enviarMsg(proceso, msg):
        try:
            s = socket.socket()
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.connect(proceso.address) #('localhost', 3000))
            #ns = socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
            #ns.connect(proceso.address)
            s.send(msg)
            s.close()
            return 1
        except:
            return 0

    def escucharMsg(self):
        #self.nom = "proces k"
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(self.address)#('', 3000))
        s.listen(1)
        while 1:
            print type(self.address), "-> ", self.address

            conn, addr = s.accept()
            print "recibida conexion de la IP: " + str(addr[0]) + " puerto: " + str(addr[1])
            thread.start_new_thread(self.connection, (sc, addr))

    def connection(self, sc, addr):
        # Solo existen tres tipos de mensajes:
        # e
        # ok
        # coordinador
        data = sc.recv(1024)

        if data == 'e':
            print "Recibi un mensaje de eleccion"
            respuesta = '1'
            sc.rend(respuesta)
        elif data == 'ok':
            print "Recibi un mensaje de OK"
            respuesta = '1'
            sc.rend(respuesta)
        elif data == 'coordinador':
            print "Recibi un mensaje de coordinador"
            respuesta = '1'
            sc.rend(respuesta)

def main():
    global procesos
    crearProceso = True
    while 1:
        if crearProceso:
            cantProcesos = input("Ingrese la cantidad de procesos: ")
            for i in range(cantProcesos):
                nom = "proceso "+str(i+1)
                prioridad = i + 1
                status = "active"
                direccion = ('localhost', 7000+10*i)

                procesoi = Proceso(nom, prioridad, status, direccion)
                procesos.append(procesoi)
                thread.start_new_thread(procesoi.escucharMsg, ())

            crearProceso = False

        # INICIAR PROCESO DE SELECCION
        for i in procesos:
            print i.mostrarProceso()
        time.sleep(4)

                #if i == cantProcesos:
                #    procesoi = Proceso(nom, prioridad, status, direccion, True)
                #    procesos.append(procesoi)
                #    thread.start_new_thread(procesoi.escucharMsg, ())#connection,(sc,addr, relojSys))
                #else:
                #    procesoi = Proceso(nom, prioridad, status, direccion)
                #    procesos.append(procesoi)
                #    thread.start_new_thread(procesoi.escucharMsg, ())

        #for i in procesos:
        #    print i.mostrarProceso()

if __name__ == '__main__':
    main()
