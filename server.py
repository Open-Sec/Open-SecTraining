# Echo Servidor
#Ejecutar : python server.py
import socket
import hashlib

HOST = ''                 # Nombre simbolico para 0.0.0.0

PORT = 50007              # Puerto no privilegiado, arbitrario
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
while 1:
	conn, addr = s.accept()
	print 'Se conecto la maquina', addr
	while 1:
	    data = conn.recv(1024)
	    if not data: break
	    h = hashlib.md5()
            h.update(data)
	    #print h.hexdigest()
	    conn.send("El MD5 Hash de lo que envio el cliente es --->"+h.hexdigest())
conn.close()
