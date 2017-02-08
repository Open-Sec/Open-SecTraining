#!/usr/bin/python

#Tumi (c) 2013 fp_zt.py

#Ejecucion CLI por ejemplo : python goodorker.py site:dominio.com > dominio.html

import httplib, re, sys, time

label  = sys.argv[1].upper()
#label viene con uno de los siguientes:
#site:dominio.com
#grupo empresarial peruano
#dominio.com -->ojo que no es lo mismo que site: para efectos como pastebin
dorks = open("./dorks.lst","r")
dorks_list = dorks.readlines()
dorks.close()


print "Google Dorking Results ===> "

if label[:5] == "SITE:":
	leading = label.replace(":","%3A")
else:
	leading = "%22"+label.replace(" ","%20")+"%22"
	
for currentDORK in dorks_list:
	dork2run = leading+" "+str(currentDORK).replace("\n","")
	#depura = "/search?&hl=en&q="+ leading + "%20" + currentDORK + "&safe=off&filter=0"
	#print depura
	h = httplib.HTTP('www.google.com')
	h.putrequest('GET',"/search?&hl=en&q="+ leading + "%20" + currentDORK + "&safe=off&filter=0")
	h.putheader('Host', 'www.google.com')
	h.putheader('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6')
	h.endheaders()
	returncode, returnmsg, headers = h.getreply()
	data=h.getfile().read()
	time.sleep(2.0)
	print data
	r1 = re.compile('<h3 class=[^>]+><a href="([^"]+)"')
	res = r1.findall(data)
	if len(res) > 0:
		r2 = re.compile('No results found for')
		res2 = r2.findall(data)
		if str(res2[0]) != 'No results found for':
			print "\n\n\nShowing just 5 first results for dork " + dork2run + "\n\n"
			for item in res[:5]:
				url=item.split('&')[0]
				url=url.split('://')[1]
				print str(url)
		else:
			print "No hay resultados exactos para el dork "  + dork2run + "\n\n"
