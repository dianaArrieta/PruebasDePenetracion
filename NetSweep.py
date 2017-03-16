#!/usr/bin/python
# -*- coding: utf-8 -*-

#Arrieta Jiménez Diana Laura#
import sys
from re import match
from subprocess import check_output,CalledProcessError



def convenoct(IP):
	IPocteto=[]
	IPocteto.insert(0,IP//16777216)
	IP = IP % 16777216
	IPocteto.insert(1,IP//65536)
	IP = IP % 65536
	IPocteto.insert(2,IP//256)
	IP = IP % 256
	IPocteto.insert(3,IP)
	return str(IPocteto[0])+'.'+str(IPocteto[1])+'.'+str(IPocteto[2])+'.'+str(IPocteto[3])

if((len(sys.argv)>1) and (sys.argv[1]=="--help" or sys.argv[1]=="h")):
	print("\tUso: NetSweep.py\n\t Este programa mostrará una lista de todos los host activos de la\n\t red en la que se encuentra el dispositivo que lo ejecuta.\n\t Si dispone de más de una interfaz de red se le pedirá que \n\t ingrese el numero de la interfaz que se usará de una lista.\n\n\t NOTA: Este programa, dependiendo de la cantidad de Host en su\n\t Segmento de Red, puede tardar unos minutos.")
	sys.exit(1)

Interfaces = []
Leido = False
LineasInterfaces = str(check_output('route -n', shell=True,universal_newlines=True)).split('\n')
cuentaLinea = 1
for linea in LineasInterfaces:
	if cuentaLinea == 1 or cuentaLinea==2 or cuentaLinea==len(LineasInterfaces):
		cuentaLinea+=1
		continue
	for inter in Interfaces:
		if inter == linea.split()[7]:
			Leido = True
	if not(Leido):
		Interfaces.append(linea.split()[7])
	Leido = False
	cuentaLinea+=1
if len(Interfaces) > 1:
	print("Se detectaron las siguientes interfaces:\n")	
	cuenta  = 0
	for inter in Interfaces:
		print(str(cuenta)+") "+inter+"\n")
		cuenta+=1
	numero = int(input("Ingrese el numero de interfaz que desea usar: "))
	if numero<0 or numero>len(Interfaces):
		print("INTERFAZ INVALIDA")
		sys.exit(1)
	interfaz = Interfaces[numero]
else:
	interfaz = Interfaces[0]

print("Interfaz Seleccionada: "+interfaz)

try:
	ifaz=check_output('ifconfig ' + interfaz + '|grep "inet:"',shell=True,universal_newlines=True).split()
except CalledProcessError:
	ifaz=check_output('ifconfig ' + interfaz + '|grep "inet addr:"',shell=True,universal_newlines=True).split()
try:
	entrada=ifaz[1][5:]
	mascara=ifaz[3][5:]
except IndexError:
	print('No se asigno un valor de ip o mascara')
	
print "Su IP: "+entrada
print "Su NetMask: "+mascara

bloquem = mascara.split('.')
bloques = entrada.split('.')
mascint = (int(bloquem[0])*16777216)+(int(bloquem[1])*65536)+(int(bloquem[2])*256)+(int(bloquem[3]))
ipint = (int(bloques[0])*16777216)+(int(bloques[1])*65536)+(int(bloques[2])*256)+(int(bloques[3]))
red = ipint & mascint
Sred = convenoct(red)
print('Su direccion de red es: \n'+Sred)
EnRed = 0
host = red
numeroh = 4294967295-mascint-1
for i in range(numeroh):
	host += 1
	Shost = convenoct(host)
	try:
		check_output('ping -c 2 '+Shost,shell=True,universal_newlines=True).split()
		print("Host activo: "+Shost)
		EnRed+=1
	except CalledProcessError:
		continue
print(str(EnRed)+" Host Activos en su red ")

