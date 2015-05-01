#!/usr/bin/python
#Autor : Walter Cuestas, @wcu35745
#Note for EC Council ECC Points
import urllib2, urllib, sys, os

if len(sys.argv) < 4:
	sys.exit("Usalo asi : " + sys.argv[0] + " archivo_gnmap archivo_files.csv_de_exploitdb (ruta completa) Cantidad_Caracteres_Banner_a_Buscar\n")
#No funciona muy bien porque los banners tienen informacion que hace la busqueda inexacta en muchos casos
#Por eso el usuario debe definir cuantos caracteres del banner se usaran en la busqueda

long_banner_2_use = int(sys.argv[3])

gnmap = open(sys.argv[1],"r+")
todas_las_lineas = gnmap.readlines()
gnmap.close()

exploitdb = open(sys.argv[2],"r+")
todos_los_exploits = exploitdb.readlines()
exploitdb.close()

for cada_linea in todas_las_lineas:
	#Separa por espacio para sacar la IP del host
	delimitador1 = cada_linea.split(' ')
	
	#Separa por dos puntos para determinar si es la linea que tiene la informacion de puertos y banners, no las de header ni Status
	delimitador2 = cada_linea.split(':')
	#Toma el segundo campo : Host --->: 190.81.188.17 ()	Ports:<-------- 8 ---- el conteo de elementos inicia en cero
	linea_ports = delimitador2[1:2]
	
	#Valida si los ultimos 7 chars dicen Ports porque asi identica que es la linea con la info
	if str(linea_ports)[-7:] == "Ports']":
		host = delimitador1[1:2]
		print "\n\033[0;31;40mHOST ---> " + str(host) + "\033[0m\n"
		
		#limite_inicio es el 7mo elemento (inicio en cero el conteo) y limite_fin es el 8vo elemento (que no lo incluye)
		limite_inicio = 6
		limite_fin = 7
		
		#Separa por / para leer cada numero de puerto, protocolo, etc. e identificar el banner
		delimitador3 = cada_linea.split('/')
		
		#Loop mientras el contador de limite_fin este dentro de la longitud de la presente linea separada por /
		while limite_fin <= len(delimitador3) :
			banner = delimitador3[limite_inicio:limite_fin]
			if str(banner) <> "['']" :
				#Para dejar solo el texto y remover ['xxx']
				label = str(banner).strip('[]').replace("'","") 
				print "\n\033[0;32;40mBANNER ---> " + label + "\033[0m\n"
				#url = 'http://www.exploit-db.com/search/?action=search&filter_page=1&filter_description=&filter_exploit_text='+str(banner).strip('[]').replace("'","")+'&filter_author=&filter_platform=0&filter_type=0&filter_lang_id=0&filter_port=&filter_osvdb=&filter_cve='
				#webbrowser.open(url,new=2,autoraise=True)
				for cada_exploit in todos_los_exploits:
					delimitadorexploit = cada_exploit.split(',')
					exploit = str(delimitadorexploit[2:3]).strip('[]').replace("'","") 
					if exploit.find(label[:long_banner_2_use]) != -1:
						exploitfile = str(delimitadorexploit[1:2]).strip('[]').replace("'","")
						exploitfound = str(delimitadorexploit[2:3]).strip('[]').replace("'","")
						print "\033[0;36;40mFILE --->\033[0m /pentest/exploits/exploitdb/" + exploitfile + " \033[0;31;40m EXPLOIT --->\033[0m " + exploitfound
			limite_inicio = limite_inicio + 7
			limite_fin = limite_fin + 7

