#!/usr/bin/python


import sys,subprocess,re,dns.resolver
if len(sys.argv) < 2:
	print "\t Uso: t_zona.py Dominio"
	sys.exit(1)
error = re.compile('; Transfer failed.')
dominio = sys.argv[1]
infile = []

ns = dns.resolver.query(dominio, 'NS')
for i in ns.response.answer:
	for j in i.items:	
		infile.append(j)

for line in infile:
	b= True
	a = '@' + str(line).rstrip(".")
	p = subprocess.Popen('dig '+ a + ' axfr '+ dominio,shell=True,stdout=subprocess.PIPE)
	salida = p.stdout.read()
	if error.search(salida):
		b = False
	if b:
		print(salida)

