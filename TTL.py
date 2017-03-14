#! /usr/bin/python
#Arrieta Jimenez Diana Laura#

import sys,subprocess,re
if len(sys.argv) < 2:
	print "\t Uso: TTL.py Host"
	sys.exit(1)
host = sys.argv[1]
ttl = -1
Busqueda = re.compile('ttl=')
cmdping = "ping "+host+" -w 5"
error = True
print "Haciendo ping al host: "+host
p=subprocess.Popen(cmdping,shell=True,stdout=subprocess.PIPE)
respuesta = p.stdout.read()
for linea in respuesta.split('\n'):
	if Busqueda.search(linea):
		separada = linea.split('ttl=') 
		valor = separada[1].split(' ')
		ttl = int(valor[0])
		error = False
if ttl>0 and ttl <= 64:
	print "Sistema Operativo: distribucion GNU/Linux o MAC OS"
if ttl>64 and ttl <= 128:
	print "Sistema Operativo: distribucion Windows"
if ttl>128 and ttl <=255:
	print "Sistema Operativo: distribucion Solaris/AIX o Cisco IOS"
if error:
	print "Error: No se alcanzo el Host "+host
