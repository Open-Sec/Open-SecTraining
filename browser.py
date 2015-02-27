#!/usr/bin/python

import urllib2
headers = { 'User-Agent' : 'Mozilla/5.0' }
solicitud = urllib2.Request('http://www.google.com/search?q=python+es+la+voz',None, headers)
respuesta = urllib2.urlopen(solicitud)
payload = respuesta.read()
print(payload)
