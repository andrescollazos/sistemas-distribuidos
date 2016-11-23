class Grafo(object):
    def __init__(self):
        self.relaciones = {}

    def __str__(self):
        for i, elem in enumerate (self.relaciones):
            print "{0} -> {1}".format(elem, self.relaciones[elem])
        return ""

    def agregar(self, elemento):
        self.relaciones.update({elemento:[]})

    def relacionar(self, origen, destino):
        self.relaciones[origen].append(destino)
        #self.relaciones[destino].append(origen)

    def eliminar(self, elemento):
        del self.relaciones[elemento]
        for i in self.relaciones:
            if self.relaciones[i] == [elemento]:
                del self.relaciones[i][0]

def recorrer(grafo, elementoInicial, elementosRecorridos = []):
    print elementoInicial, "->",
    elementosRecorridos.append(elementoInicial)
    try:
        for vecino in grafo.relaciones[elementoInicial]:
            recorrer(grafo, vecino, elementosRecorridos)
    except KeyError:
        pass



# PARAMETROS LOCALES

S = "S"
R = "R"
T = "T"
A = "A"
B = "B"
C = "C"

grafo = Grafo()
grafo.agregar(S)
grafo.agregar(R)
grafo.agregar(T)
grafo.agregar(A)
grafo.agregar(B)
grafo.agregar(C)

grafo.relacionar(T, C)
grafo.relacionar(C, S)
grafo.relacionar(S, A)
grafo.relacionar(A, R)
grafo.relacionar(R, B)

print grafo

recorrer(grafo, C)
