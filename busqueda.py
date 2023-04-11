import sys
import random
from collections import defaultdict
from copy import deepcopy
from queue import PriorityQueue as pqueue



solOptima = -1
h = []

# lectura del input
def leer():
	f = open(sys.argv[1], "r")

	h = dict()
	adj = defaultdict(dict)

	l = 0
	for linea in f:
		cosas = linea.split()

		if l == 0:
			ni = cosas[1]
			l += 1

		elif l == 1:
			nf = cosas[1]
			l += 1

		elif len(cosas) == 2:
			h[cosas[0]] = int(cosas[1]) 

		else:
			n1, n2, c = cosas[0][0], cosas[1][0], int(cosas[2])
			adj[n1][n2] = c

	return ni, nf, h, adj

# impresion de resultados
def imprimir(camino, adj, exp, nf):
	# verificar si es solucion o no
	if not len(camino) or camino[-1] != nf:
		print("Sin solucion")
		return
	
	costo = 0
	for i in range(len(camino)):
		if camino[i] == nf: 
			print(camino[i])
		else:
			print(camino[i] + " -> ", end = '')
			costo += adj[camino[i]][camino[i+1]]

	print("Costo:", costo)
	global solOptima
	if costo == solOptima:
		print("Solucion optima")
	else:
		print("Solucion no optima")

	global h
	for n in h:
		print(n + ":", exp.count(n))

# Busqueda en profundidad
def profundidad(ni, nf, adj):
	visitado = []
	camino = []
	profundidadRec(ni, nf, deepcopy(adj), camino, visitado)

	print()
	print("Busqueda en profundidad")

	imprimir(camino, adj, visitado, nf)

def profundidadRec(actual, nf, adj, camino, visitado):
	visitado.append(actual)
	camino.append(actual)

	if actual == nf:
		return True

	while len(adj[actual]):
		# elegir un elemento aleatorio adyacente al nodo actual
		# y sacarlo para no volver a elegirlo
		sig = random.choice(list(adj[actual]))
		del adj[actual][sig]

		# visitar el nodo elegido si no ha sido visitado
		if sig not in visitado:
			if profundidadRec(sig, nf, adj, camino, visitado):
				return True
	
	# si llego aca es porque el camino llego a fin
	camino.pop()
	return False

# Busqueda Greedy
def greedy(ni, nf, adj, h):
	camino = []

	actual = ni
	while True:
		camino.append(actual)
		# terminar si llego al objetivo o termino en un camino cerrado
		if not len( adj[actual] ) or actual == nf:
			break
		
		# elegir el nodo adyacente al actual con la menor heuristica
		hmin = float("inf")
		for n in adj[actual]:
			if h[n] < hmin:
				hmin = h[n]
				sig = n

		actual = sig

	print()
	print("Busqueda Greedy")
	imprimir(camino, adj, camino, nf)

# Busqueda costo uniforme
def uniforme(ni, nf, adj):
	camino = []
	pq = pqueue()

	pq.put( (0, ni) )

	while not pq.empty():
		# elegir el nodo en la cola con menor costo
		c, actual = pq.get()
		camino.append(actual)

		# terminar si llego al objetivo
		if actual == nf:
			break
		
		# poner en la cola los costos hacia nodos adyacentes
		for n in adj[actual]:
			if n not in camino:
				pq.put( (adj[actual][n], n) )

	print()
	print("Busqueda por costo uniforme")
	imprimir(camino, adj, camino, nf)

# Busqueda A*
def A(ni, nf, adj, h):
	# poner el valor de la funcion de cada nodo en infinito
	funcion = dict()
	for n in h:
		funcion[n] = float("inf")

	funcion[ni] = h[ni]

	# costo total de viaje desde el nodo inical al nodo n
	costo = dict()
	costo[ni] = 0

	# nodos a explorar
	pq = pqueue()

	padre = dict() 	# nodo padre del nodo n
	exp = []		# nodos expandidos

	pq.put( (0, ni) )
	while not pq.empty():
		# elegir el nodo con menor valor de funcion de "hojas"
		c, actual = pq.get()

		exp.append(actual)

		# terminar si llego al objetivo
		if actual == nf:
			break
		
		# calcular el valor de la funcion para cada nodo adyacente al actual
		for n in adj[actual]:
			f = costo[actual] + adj[actual][n] + h[n]

			# actualizar el valor de la funcion si es que se mejora y añadirlo a "hojas"
			if f < funcion[n]:
				padre[n] = actual
				funcion[n] = f
				costo[n] = costo[actual] + adj[actual][n]
				pq.put( (f, n) )


	# armar el camino si encontro uno
	camino = []
	if nf in padre:
		actual = nf
		while actual != ni:
			camino.append(actual)
			actual = padre[actual]

		camino.append(ni)

	camino.reverse()
	global solOptima
	solOptima = costo[nf]

	print()
	print("Busqueda A*")
	imprimir(camino, adj, exp, nf)



# nodo inicial, nodo final, valor heuristica, nodos adyacentes
ni, nf, h, adj = leer()

A(ni, nf, adj, h)
profundidad(ni, nf, adj)
greedy(ni, nf, adj, h)
uniforme(ni, nf, adj)





	
