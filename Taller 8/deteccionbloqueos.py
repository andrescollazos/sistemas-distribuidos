import sys

conexiones = [
    ("A", "S"),
    ("B", "T"),
    ("C", "S"),
    ("D", "S"), ("D", "W"), ("D", "T"),
    ("E", "V"),
    ("F", "S"),
    ("G", "U"),
    ("R", "A"),
    ("T", "E"),
    ("U", "D"),
    ("V", "G"),
    ("W", "F")
]

lista_marcados = [
    ("A", False),
    ("B", True),
    ("C", False),
    ("D", False),
    ("E", False),
    ("F", False),
    ("G", False),
    ("R", False),
    ("T", False),
    ("U", False),
    ("V", False),
    ("W", False),
]

# Buscar un nodo que no este marcado para iniciar:
def iniciar(lista_marcados):
    for i in lista_marcados:
        if not i[1]:
            return i[0]
            break

# Funcion para Verificar que un nodo tiene conexiones de salida:
def tieneConexiones(conexiones, nodo):
    cont = 0
    for i in conexiones:
        if nodo == i[0]:
            cont = cont + 1

    if cont == 0:
        return False
    else:
        return True

def recorrer(conexiones, lista_marcados, nodoinicial, lista):
    # Nodo actual
    nodoi = nodoinicial
    lista.append(nodoi)
    nodoant = lista[lista.index(nodoi) - 1]
    #print "NODO: ", nodoi
    # Marcar nodo como visitado:
    for x, i in enumerate(lista_marcados):
        #print "nodo: ", nodoi, " i:", i
        if nodoi == i[0]:
            lista_marcados[x] = (nodoi, True)

    # IMPRIMIR RECORRIDOS DE ESTA ITERACION:
    print "---------------------"
    print lista
    print "Nodo actual: ", nodoi, " Nodo anterior: ", nodoant
    print "---------------------"

    #Verificar que el nodo si tenga conexiones:

    if tieneConexiones(conexiones, nodoi):
        for i in conexiones:
            if nodoi == i[0]:
                #print i
                recorrer(conexiones, lista_marcados, i[1], lista)
    else:
        print "No hay conexiones de la salida para {0} ..".format(nodoi)
        #nuevo_nodo = iniciar(lista_marcados)
        print "Devolverse al nodo anterior con: ", nodoant

        recorrer(conexiones, lista_marcados, nodoant, [])


recorrer(conexiones, lista_marcados, "R", [])
