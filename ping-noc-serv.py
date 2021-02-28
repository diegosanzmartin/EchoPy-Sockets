#SERVER UDP

import signal, socket, sys, os
from time import time

ERR = "\033[93m"
END = "\033[0m"

if __name__ == "__main__":
    if len(sys.argv) != 2 :
        print(ERR + "ERR: Nº de argumentos no válidos" + END)
        sys.exit()
    
    #Variables socket
    servIP = "127.0.0.1"
    servPort = int(sys.argv[1])
    bufferSize = 1024

    if servPort < 1023:
        print(ERR + "ERR: El nº de puerto debe ser mayor que 1023" + END)
        sys.exit()

    #Creación del socket UDP
    servSock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) #familia -> IPv4, tipo de socket -> UDP
    
    #Conexión socket
    servSock.bind((servIP, servPort))
    while True:
        try:
            #Recibo datos del servidor
            dataRecv = servSock.recvfrom(bufferSize)
            start = time()
            mss = dataRecv[0]
            add = dataRecv[1]

            #Envío respuesta a cliente
            servSock.sendto(mss, add)
            t = time() - start

            print("-Servidor: %s bytes= %d time= %f" %(add, len(mss),t))

        except KeyboardInterrupt:
            print("\n------Estadísticas------\n")
            sys.exit()