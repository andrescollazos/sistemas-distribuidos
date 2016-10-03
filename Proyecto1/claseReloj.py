#!/usr/bin/python
import time
import thread

class Reloj():
    def __init__(self):
        self.hora = 0
        self.minuto = 0
        self.segundo = 0
        self.milisegundo = 0

    def setHora(self, hora, minuto, segundo, milisegundo=0):
        self.hora = hora
        self.minuto = minuto
        self.segundo = segundo
        self.milisegundo = milisegundo

    def retHora(self):
        horaRetornar = 0
        if len(str(self.hora)) == 1:
            horaRetornar = "0"+str(self.hora)+":"
        else:
            horaRetornar = str(self.hora)+":"

        if len(str(self.minuto)) == 1:
            horaRetornar = horaRetornar + "0"+str(self.minuto)+":"
        else:
            horaRetornar = horaRetornar + str(self.minuto)+":"

        if len(str(self.segundo)) == 1:
            horaRetornar = horaRetornar + "0"+str(self.segundo)+":"
        else:
            horaRetornar = horaRetornar + str(self.segundo)+":"

        if len(str(self.milisegundo)) == 1:
            horaRetornar = horaRetornar + "0"+"0"+str(self.milisegundo)
        elif len(str(self.milisegundo)) == 2:
            horaRetornar = horaRetornar + "0"+str(self.milisegundo)
        elif len(str(self.milisegundo)) == 3:
            horaRetornar = horaRetornar + str(self.milisegundo)

        return horaRetornar

    def mostrarHora(self):
        print "{0}:{1}:{2}:{3}".format(self.hora,self.minuto, self.segundo, self.milisegundo)


    def tick(self):
        while True:
            while self.hora < 24:
                while self.minuto < 60:
                    while self.segundo < 60:
                        while self.milisegundo < 1000:
                            time.sleep(0.001)
                            #self.mostrarHora()
                            self.milisegundo = self.milisegundo + 1
                        self.milisegundo, self.segundo = 0, self.segundo + 1
                    self.segundo, self.minuto = 0, self.minuto + 1
                self.minuto, self.hora = 0, self.hora + 1
            self.hora = 0
