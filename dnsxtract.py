#!/usr/bin/python
#Autor : Walter Cuestas Agramonte @wcu35745
#Note for EC Council ECC Points

#import dns.query
import dns.zone
import dns.resolver
import sys

#1. encontrar servidor dns
buscaNS = dns.resolver.query(sys.argv[1], 'NS')
ns1 = buscaNS[0]
ns1_ip = dns.resolver.query(str(ns1))
#ns2 = buscaNS[1]

#2. intentar zone transfer
try :
	#raise Exception ("ZT")
	transfiereZONA = dns.zone.from_xfr(dns.query.xfr(str(ns1), sys.argv[1], timeout=5, lifetime=10))
	nombresDNS = transfiereZONA.nodes.keys()
	nombresDNS.sort()
	for hosts in nombresDNS:
		print transfiereZONA[hosts].to_text(hosts)
except :
	print "Zone Transfer failed.  Cool!"
	
	#3. hacer busqueda con diccionario
	dictionary = open("/var/www/tumi/tools/nombreshosts.dict","r+")
	todas_las_lineas = dictionary.readlines()
	dictionary.close()

	#Que no lea /etc/resolv.conf
	resolverinstance = dns.resolver.Resolver(configure=False)
	#Convertir elemento de lista en string y luego armar la otra lista porque debe ser una lista de strings.
        resolverinstance.nameservers = [str(ns1_ip[0]),]
	
	for host in todas_las_lineas:
		node = host.replace("\n","") + "." + sys.argv[1]
		try:
			buscaHOST = resolverinstance.query(node,'A')
			print "Found Node! : " + node + "-->" + str(buscaHOST[0])
		except:
			try:
				buscaCNAME = resolverinstance.query(node,'CNAME')
				aliasNODE = str(buscaCNAME[0])[:-1]
                        	print "Alias Node Found! : " + node + "-->" + aliasNODE
				#Obtiene registro A del origen del CNAME
				buscaHOST2 = dns.resolver.query(aliasNODE,'A')
				print "Found Node! : " + aliasNODE + "-->" + str(buscaHOST2[0])
			except:
				pass
			pass
