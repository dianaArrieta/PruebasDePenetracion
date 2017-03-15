#! /usr/bin/python
#Arrieta Jimenez Diana Laura#
import socket,sys
if (len(sys.argv) < 4) or ( sys.argv[3] < sys.argv[2]):
	print "\t Uso: Puertos.py Host PuertoInicio PuertoFin"
	sys.exit(1)
inicio = int(sys.argv[2])
fin = int(sys.argv[3])
host = sys.argv[1]
contador = 0
soc = socket.socket()
for puerto in range(inicio,fin):
	try:
		soc.connect((host,puerto))
		print "Puerto abierto: "+str(puerto)
		soc.close()
		soc = socket.socket()
		contador += 1
	except socket.error, exc:
		if(exc.errno == 113):
			print "No se puede alcanzar el host "+host
			sys.exit(1)
if contador == 0:
	print "Ningun puerto se detecto abierto en el host "+host
else:
	print str(contador)+" puertos se encontraron abiertos en el host "+host
