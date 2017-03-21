#! /usr/bin/python
# -*- coding: utf-8 -*-

#Arrieta Jimenez Diana Laura#


import socket,sys
from struct import *
if len(sys.argv)>1  and (sys.argv[1]=='--help' or sys.argv[1]=='h'):
	print "\tUSO: VentanaTCP.py\n\n\t Este programa es un sniffer de paquetes TCP, \n\t si se detecta un tamaño de ventana estandar\n\t para un sistema operativo, se notificará que\n\t sistema operativo esta siendo utilizado en el\n\t HOST que mandó el paquete."
	sys.exit(1)
ipvistas =[]
yavista = False
sistemas = []
s=socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname('tcp')) 

print"Leyendo paquetes TCP: \n"
while True:
    #se leen 65565 bytes del paquete (tamaño maximo que puede tener TCP)
    packet = s.recvfrom(65565)
     
    #packet string from tuple
    packet = packet[0]
     
    #take first 20 characters for the ip header
    ip_header = packet[0:20]
     
    #now unpack them :)
    iph = unpack('!BBHHHBBH4s4s' , ip_header)
     
    version_ihl = iph[0]
    version = version_ihl >> 4
    ihl = version_ihl & 0xF
     
    iph_length = ihl * 4
    s_addr = socket.inet_ntoa(iph[8]);
    d_addr = socket.inet_ntoa(iph[9]);
    #Leer el header de TCP     
    tcp_header = packet[iph_length:iph_length+20]
     
    #decempaquetarlo
    tcph = unpack('!HHLLBBHHH' , tcp_header)
#se divide por byte:224411222 
    #se saca cada parte de la cabecera
    source_port = tcph[0]
    dest_port = tcph[1]
    sequence = tcph[2]
    acknowledgement = tcph[3]
    doff_reserved = tcph[4]
    tcph_length = doff_reserved >> 4
    reserved = (doff_reserved & 0xF)>> 1
    flags = tcph[5]
    wsize = tcph[6]
    checksum = tcph[7]
    urgentpoint = tcph[8]
    #Verificar que sea el primer mensaje TCP de la ip
    for ips in ipvistas:
        if ips == s_addr:
            yavista=True
    #Comparar el tamaño de la ventana con unos ya cconocidos por Sistemas Operativos (Pendiente a expandirse)
    if not (yavista):
        if wsize == 5840:
            print 'Paquete TCP detectado proveniente del host: '+s_addr+', Sistema Operativo: Linux (Kernel 2.4 o 2.6)'
        elif wsize == 5720:
            print 'Paquete TCP detectado proveniente del host: '+s_addr+', Sistema Operativo: Linux, modificado por Google'
        elif wsize == 65535:
            print 'Paquete TCP detectado proveniente del host: '+s_addr+', Sistema Operativo: FreeBSD o Windows XP'
        elif wsize == 8192:
            print 'Paquete TCP detectado proveniente del host: '+s_addr+', Sistema Operativo: Windows Vista | 7 | 8 o Windows Server 2008 | 2012'
        elif wsize == 4128:
            print 'Paquete TCP detectado proveniente del host: '+s_addr+', Sistema Operativo: Cisco iOS 12.4'
        ipvistas.append(s_addr)
    yavista=False

