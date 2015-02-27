#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import string
import httplib, sys
from socket import *
import re
import getopt

print "\n*************************************"
print "*TheHarvester Ver. 1.5              *"
print "*Coded by Christian Martorella      *"
print "*Edge-Security Research             *"
print "*cmartorella@edge-security.com      *"
print "*Modified by Open-Sec 09092012      *"
print "*************************************\n\n"

#Cambios del 09092012
#Habia adicionado a las busquedas que usan Google las dobles comillas (linkedin) en el codigo para no tener que tipearlas y porque
#reducian la cantidad de falsos positivos, pero, comparado con versiones recientes de theHarvester de edge-security, se estaban
#dejando de encontrar varios resultados (diferencia de 21 a 8).  Quite las dobles comillas del codigo solo para Linkedin, arroja
#falsos positivos que se deben quitar a mano, pero, saca mas positivos reales que cualquier otra version.  la remocion de los falsos 
#positivos sera en HIDE.
#Tambien, en las busquedas con Bing se quito la palabra "of" del conteo de ocurrencias y un espacio en blanco despues del email al filtrar
#las cuentas de correo porque ya no son usados por Bing.

global word
global w
global result
result = []

def usage():

 print "Usage: theharvester options \n"
 print "       -d: domain to search or company name"
 print "       -b: data source (google,bing,pgp,linkedin)"
 print "       -l: limit the number of results to work with(bing goes from 50 to 50 results,"
 print "            google 100 to 100, and pgp does'nt use this option)"
 print "\nExamples:./theharvester.py -d microsoft.com -l 500 -b google"
 print "         ./theharvester.py -d microsoft.com -b pgp"
 print "         ./theharvester.py -d microsoft -l 200 -b linkedin\n"

def howmanymsn(w):
	h = httplib.HTTP('www.bing.com')
	h.putrequest('GET', "/search?q=%40" + w + "&go=&FORM=QBHL&qs=n")
	h.putheader('Host', 'www.bing.com')
	h.putheader('User-agent', '(Mozilla/5.0 (Windows; U; Windows NT 6.0;en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6')	
	h.putheader('Cookie: mkt=en-US;ui=en-US')
	h.putheader('Accept-Language: en-us,en')
	h.endheaders()
	returncode, returnmsg, headers = h.getreply()
	data = h.getfile().read()
	#print data
	r1 = re.compile('[0123456789,.]* results')
	result = r1.findall(data)
	#print result
	for x in result:
		#clean = re.sub('of', '', x)
		clean = re.sub('results', '', x)
		clean = string.replace(clean, '.', ',')
		clean = re.sub(',', '', clean)
	return clean

def howmanygoogle(w):
		h = httplib.HTTP('www.google.com')
		# By Open-Sec
		# Added double quotes around w to get less false positives in serach result
		if engine == "google":
				h.putrequest('GET', "/search?hl=en&meta=&client=safari&rls=en&q=\"%40" + w + "\"")
		else:
				#h.putrequest('GET', "/search?hl=en&meta=&q=site%3Alinkedin.com%20" + w)
				h.putrequest('GET', "/search?hl=en&meta=&q=site%3Alinkedin.com%20\"" + w + "\"")
		h.putheader('Host', 'www.google.com')
		h.putheader('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.0; ru; rv:1.9.2) Gecko/20100115 Firefox/3.6')
		h.endheaders()
		returncode, returnmsg, headers = h.getreply()
		data = h.getfile().read()
		#print data
		#By Open-Sec
		#Updated text about search results
		if engine == "google":
			r1 = re.compile('About [0123456789,]* results')
		else:
			r1 = re.compile('About [0123456789,]* results')
		result = r1.findall(data)
		for x in result:
				clean = re.sub(' <b>', '', x)
				clean = re.sub('</b> ', '', clean)
				clean = re.sub('About', '', clean)
				#clean = re.sub('for', '', clean)
				clean = re.sub(',', '', clean)
				#clean = re.sub('from', '', clean)
				clean = re.sub('results', '', clean)
		print clean
		return clean

def run_msn(w, i):
	h = httplib.HTTP('www.bing.com')
	h.putrequest('GET', "/search?q=%40" + w + "&go=&FORM=QBHL&qs=n&first="+ str(i))
	h.putheader('Host', 'www.bing.com')
	h.putheader('User-agent', '(Mozilla/5.0 (Windows; U; Windows NT 6.0;en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6')	
	h.putheader('Cookie: mkt=en-US;ui=en-US;NRSLT=50')
	h.putheader('Accept-Language: en-us,en')
	h.endheaders()
	returncode, returnmsg, headers = h.getreply()
	data = h.getfile().read()
	#print data
	data = string.replace(data, '<strong>', '')
 	data = string.replace(data, '</strong>', '')
	r1 = re.compile('[a-zA-Z0-9.-_]*' + '@' + '[a-zA-Z0-9.-]*' + w + ' ')
	res = r1.findall(data)
	return res

def run(w, i, eng):
	if eng == "bing":
		h = httplib.HTTP('www.bing.com')
		h.putrequest('GET', "/search?q=%40" + w + "&go=&FORM=QBHL&qs=n&first="+ str(i))
		h.putheader('Host', 'www.bing.com')
		h.putheader('Cookie: mkt=en-US;ui=en-US;SRCHHPGUSR=NEWWND=0&ADLT=DEMOTE&NRSLT=50')
		h.putheader('Accept-Language: en-us,en')
	if eng == "linkedin":
		h = httplib.HTTP('www.google.com')
		# By Open-Sec
                # Added double quotes around w to get less false positives in serach result
		h.putrequest('GET', "/search?num=100&start=" + str(i) + "&hl=en&meta=&q=site%3Alinkedin.com%20\"" + w + "\"")
		#h.putrequest('GET', "/search?num=100&start=" + str(i) + "&hl=en&meta=&q=site%3Alinkedin.com%20" + w)
		h.putheader('Host', 'www.google.com')
	elif eng == "google":
		h = httplib.HTTP('www.google.com')
		# By Open-Sec
                # Added double quotes around w to get less false positives in serach result
		h.putrequest('GET', "/search?num=100&start=" + str(i) + "&hl=en&meta=&q=%40\"" + w + "\"")
		h.putheader('Host', 'www.google.com')
	elif eng == "pgp":
		h = httplib.HTTP('pgp.rediris.es:11371')
		h.putrequest('GET', "/pks/lookup?search=" + w + "&op=index")
		h.putheader('Host', 'pgp.rediris')
	h.putheader('User-agent', '(Mozilla/5.0 (Windows; U; Windows NT 6.0;en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6')	
	h.endheaders()
	returncode, returnmsg, headers = h.getreply()
	data = h.getfile().read()
	#print data
	if eng == "bing":
 		data = string.replace(data, '<strong>', '')
 		data = string.replace(data, '</strong>', '')
		for e in ('>', ':', '=', '<', '/', '\\', ';','&'):
			data = string.replace(data, e, ' ')
	elif eng == "google":
		data = re.sub('<b>', '', data)
		data = re.sub('<em>', '', data)
		for e in ('>', ':', '=', '<', '/', '\\', ';'):
			data = string.replace(data, e, ' ')
	elif eng == "linkedin":
	        #re1 = re.compile('class=l>[a-zA-Z ,._-]* - LinkedIn</a>')
		#re1 = re.compile('>[a-zA-Z ,._-]* - LinkedIn</a>')
		#By Open-Sec
		# Removed Directory word becuase there are Spanish results with Directorio and "country" Directorio
		# Also, escaped the pipe because it's an OR for python regular expression in compile
		# Para aquellos que no tienen el pipe sino guion, hay que reemplazarlo
		# Algunos tienen resaltado Banco Ripley en el resultado de la busqueda con Google y eso adiciona <em>Banco Ripley</em>
		# hay que ver de concatenar resultados de los usan pipe + guion + em y aun asi no consigo que aparezca en los resultados 
		# >Igor Grimaldo - Product Manager at <em>Banco Ripley</em> Perú |  LinkedIn</a>
		re1 = re.compile('>[a-zA-Z ,._-]* - [a-zA-Z áéíóú]* \| LinkedIn</a>')
		res = re1.findall(data)
		#print data
		#print res
		resul = []
		for x in res:
				#print x
				y = string.replace(x, ' | LinkedIn</a>', '')
				#By Open-Sec
				#Correct sequence in cleaning results can't include x again
				y = string.replace(y, '- Directory', '')
				y = string.replace(y, '>', '')
				y = string.replace(y, '</a>', '')
				#print y
				resul.append(y)
		return resul
	else:
		data = string.replace(data, '&lt;', ' ')
		data = string.replace(data, '&gt;', ' ')
	r1 = re.compile('[a-zA-Z0-9.-_]*' + '@' + '[a-zA-Z0-9.-]*' + w)
	r2 = re.compile('[a-zA-Z0-9.-_]*' + '_at_' + '[a-zA-Z0-9.-]*' + w)
	res2=r2.findall(data)
	#print res2 revisar _at_
	res = r1.findall(data)
	return res

def test(argv):
	global limit
	limit = 100
	if len(sys.argv) < 4:
		usage()
		sys.exit()
	try :
	       opts, args = getopt.getopt(argv, "l:d:b:")
	except getopt.GetoptError:
  	     	usage()
		sys.exit()
	for opt, arg in opts :
       		if opt == '-l' :
       			limit = int(arg)
    	   	elif opt == '-d' :
			word = arg
		elif opt == '-b':
			global engine
			engine = arg
			if engine not in ("bing", "google", "linkedin", "pgp", "all"):
				usage()
				print "Invalid search engine, try with: bing, google, linkedin, pgp"
				sys.exit()

	print "Searching for " + word + " in " + engine + " :"
	print "======================================\n"
	if engine == "bing":
		total = int(howmanymsn(word))
	elif engine == "google":
		total = int(howmanygoogle(word))
	elif engine == "linkedin":
		word = word.replace(' ', '%20')
		total = int(howmanygoogle(word))
	else:
		res = run(word, 0, engine)
		if res == "":
			print "0 account found"
		else:
			for x in res:
				print x
			sys.exit()
	print "Total results: ", total
	cant = 0
	if total < limit:
 			limit = total
	print "Limit: ", limit
	while cant < limit:
		print "Searching results: " + str(cant) + "\r"
		res = run(word, cant, engine)
		for x in res:
	                if result.count(x) == 0:
               		        result.append(x)
		if engine == 'google':
			cant += 100
		elif engine == 'bing':
			cant += 50
		elif engine == 'linkedin':
			cant += 100

	print "\nAccounts found:"
	print "====================\n"
	t = 0
	for x in result:
		x = re.sub('<li class="first">', '', x)
		x = re.sub('</li>', '', x)
		print x
		t += 1
	print "====================\n"
	print "Total results: ", t

if __name__ == "__main__":
        try: test(sys.argv[1:])
	except KeyboardInterrupt:
		print "Search interrupted by user.."
	except:
		sys.exit()
