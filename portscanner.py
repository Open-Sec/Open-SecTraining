# Echo Cliente
# Ejecutar : python portscanner.py direccion_ip puerto_inicial puerto_final
import socket,sys

HOST = sys.argv[1]    # El host remoto
PORT1 = int(sys.argv[2])
PORT2 = int(sys.argv[3])
currentport = PORT1
stream = "SeguridadOfensiva\n\n"

while (currentport <= PORT2) :
    try:
        print currentport
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, currentport))
        s.send(stream)
        #s.settimeout(5.0)
        data = s.recv(1024)
        #data = "dummy"
        s.close()
        print 'Puerto --->',currentport,'Abierto.  ---> Software :',repr(data)
    except:
        print 'Puerto --->',currentport,"Cerrado o Filtrado"
    currentport = currentport + 1
