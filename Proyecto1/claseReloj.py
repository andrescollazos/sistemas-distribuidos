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

    # RETORNAR CADENA: 00:00:00:000
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

    # METODO PARA AJUSTAR LA HORA
    # INPUT: (3, 20, 0, 3).ajustarHora(0,1,59,1001) -> Se quiere aumentar al reloj 1 minuto con 59 segundos y 1001 milisegundos
    # OUTPUT: (3, 22, 00, 4)
    def ajustarHora(self, h, m, s, ms):
        if self.milisegundo + ms < 1000:
            self.milisegundo = self.milisegundo + ms
        elif self.milisegundo + ms == 1000:
            self.milisegundo = 0
            self.segundo = self.segundo + 1
        else:
            if (self.milisegundo + ms) - 1000 >= 1000:
                self.ajustarHora(0, 0, 1, (self.milisegundo + ms) - 1000)
            else:
                self.milisegundo = (self.milisegundo + ms) - 1000
                self.segundo = self.segundo + 1

        if self.segundo + s < 60:
            self.segundo = self.segundo + s
        elif self.segundo + s == 60:
            self.segundo = 0
            self.minuto = self.minuto + 1
        else:
            if (self.segundo + s) - 60 >= 60:
                self.ajustarHora(0, 1, (self.segundo + s) - 60, 0)
            else:
                self.segundo = (self.segundo + s) - 60
                self.minuto = self.minuto + 1

        if self.minuto + m < 60:
            self.minuto = self.minuto + m
        elif self.minuto + m == 60:
            self.minuto = 0
            self.hora = self.hora + 1
        else:
            if (self.minuto + m) - 60 >= 60:
                self.ajustarHora(1, (self.minuto + m) - 60, 0, 0)
            else:
                self.minuto = (self.minuto + m) - 60
                self.hora = self.hora + 1

        if self.hora + h < 24:
            self.hora = self.hora + h
        else:
            self.hora = (self.hora + h) - 24

    def desface(self, reloj2):
        hora = (self.hora - reloj2.hora)*3600
        #print "h: ", self.hora, reloj2.hora, (self.hora - reloj2.hora)*3600

        minuto = (self.minuto - reloj2.minuto)*60
        #print "m: ", self.minuto, reloj2.minuto, (self.minuto - reloj2.minuto)*60

        segundo = self.segundo - reloj2.segundo
        #print "s: ", self.segundo, reloj2.segundo, self.segundo - reloj2.segundo

        milisegundo = (self.milisegundo - reloj2.milisegundo)*1.0/1000
        #print "ms: ", self.milisegundo, reloj2.milisegundo, (self.milisegundo - reloj2.milisegundo)*1.0/1000

        #print hora + minuto + segundo + milisegundo
        return hora + minuto + segundo + milisegundo


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
