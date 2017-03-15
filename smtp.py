#!/usr/bin/python

#ARRIETA JIMENEZ DIANA LAURA
import sys,re,socket

if (len(sys.argv) < 3):
	print "\t Uso: smtp.py ip username"
	sys.exit(1)
ip = sys.argv[1]
usuario = sys.argv[2]
si = re.compile('500')

try:
	s = socket.socket()
	s.connect((ip,25))
	print s.recv(512)
	s.sendall("VRFY " + usuario + " \n")
	rec = s.recv(512)
except socket.error, exc:
	if(exc.errno == 113):
		print "No se puede alcanzar el host "+ip
		sys.exit(1)

if re.match("252",rec):
	print "user -> " + usuario + " : Existe"
if re.match("550",rec):
	print "user -> " + usuario + " : No existe"

s.close()
