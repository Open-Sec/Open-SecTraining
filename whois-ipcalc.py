#!/usr/bin/python
import sys, os, StringIO, ipcalc

#if len(sys.argv) < 2:
#	sys.exit("Usalo asi : " + sys.argv[0] + " direccion_IP\n")

#gnmap = open(sys.argv[1],"r+")
#todas_las_lineas = gnmap.readlines()
#gnmap.close()

whois = "whois "+sys.argv[1]

a = os.popen(whois).read()

todas_las_lineas = StringIO.StringIO(a)

for cada_linea in todas_las_lineas:
	#Separa por slash para sacar la mascara
	delimitador1 = cada_linea.split('/')
	
	#Separa por dos puntos para sacar la IP/mascara
	delimitador2 = cada_linea.split(':')
	#Busca la linea inetnum:
	linea_inetnum = str(delimitador1[0:1]).strip('[]').replace("'","")[:8]
		
	#Valida si los primeros 8 chars dicen inetnum: porque asi identica que es la linea con la info
	if linea_inetnum == "inetnum:":
		mascara = str(delimitador1[1:2]).strip('[]').replace("'","")[:2]
		#print mascara
		#Valida si es una supernet...
		if int(mascara) < 24 :
			print "Es una supernet no asignada"
			exit()
		inetnum =ipcalc.Network(str(delimitador2[1:2]).strip('[]').replace("'","").replace("\\n",""))
		print "Direccion IP del primer Host:"+str(inetnum.host_first())
		print "Direccion IP del ultimo Host:"+str(inetnum.host_last())wcuestas@31337:~/ehtoolz/open-sec$
