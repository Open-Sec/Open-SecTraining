# Echo Cliente
# Ejecutar : python client.py "Hola Mundo"
import socket,sys

HOST = '127.0.0.1'    # El host remoto
PORT = 50007              # El puerto en que escucha el server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.send(sys.argv[1])
data = s.recv(1024)
s.close()
print 'Recibiendo desde el Servidor...', repr(data)
