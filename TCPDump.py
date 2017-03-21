#! /usr/bin/python
# -*- coding: utf-8 -*-

#Arrieta Jimenez Diana Laura#


import socket,sys,time
from struct import *
if len(sys.argv)>1  and (sys.argv[1]=='--help' or sys.argv[1]=='h'):
	print "\tUSO: VentanaTCP.py\n\n\t Este programa es un sniffer de paquetes TCP, \n\t en cuanto se detecte un paquete se mostrará\n\t en pantalla datos sobre el paquete como lo son\n\t Hora en que se capturó, IP origen>destino\n\t Puerto Origen > Destino, ACK, Secuencia y tamaño \n\t del paquete."
	sys.exit(1)
ipvistas =[]
yavista = False
sistemas = []
s=socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname('tcp')) 

print"Leyendo paquetes TCP: \n"
while True:
    #se leen 65565 bytes del paquete (tamaño maximo que puede tener TCP)
    packet = s.recvfrom(65565)
     
    #Se lee unicamente el paquete (el comando regresa tambien una IP de origen)
    packet = packet[0]
     
    #Se leen los primeros 20 bytes (cabecera IP)
    ip_header = packet[0:20]
     
    #Se desempaqueta, contemplando los tamaños estandar del contenido de la cabecera IP
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
    banderas = '['
    flags = tcph[5]
    if(reserved & 0x1) == 0x1:
        banderas = banderas+'NS'
    if(flags & 0x80) == 0x80:
        banderas = banderas+',CWR'
    if(flags & 0x40) == 0x40:
        banderas = banderas+',ECE'
    if(flags & 0x20) == 0x20:
        banderas = banderas+',URG'
    if(flags & 0x10) == 0x10:
        banderas = banderas+',ACK'
    if(flags & 0x8) == 0x8:
        banderas = banderas+',PSH'
    if(flags & 0x4) == 0x4:
        banderas = banderas+',PST'
    if(flags & 0x2) == 0x2:
        banderas = banderas+',SYN'
    if(flags & 0x1) == 0x1:
        banderas = banderas+',FIN'
    banderas=banderas+']'
    wsize = tcph[6]
    checksum = tcph[7]
    urgentpoint = tcph[8]
    #Verificar que sea el primer mensaje TCP de la ip
    for ips in ipvistas:
        if ips == s_addr:
            yavista=True
    #Si no se ha visto esa IP, comenzar a imprimir los datos leidos
    #if not (yavista):
    hora = time.strftime("%H:%M:%S")
    print hora +' IP: '+s_addr+' > '+d_addr+' PORT: '+str(source_port)+' > '+str(dest_port)+' SECUENCIA '+str(sequence)+' ACK: '+str(acknowledgement)+' Banderas: '+banderas+' Tamaño Paquete: '+str(len(packet)) 
    ipvistas.append(s_addr)
    yavista=False

