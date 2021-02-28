#SERVER UDP

import signal, socket, sys, os
from time import time
from time import sleep

ERR = "\033[93m"
END = "\033[0m"

def timeEstad(t, tmin, tmax):
    if tmax == 0.0 and tmin == 0.0:
        return t, t
    elif t > tmax:
        return tmin, t
    elif t < tmin:
        return t, tmax
    else:
        return tmin, tmax


if __name__ == "__main__":
    if len(sys.argv) != 3 :
        print(ERR + "ERR: Nº de argumentos no válidos" + END)
        sys.exit()
    
    #Variables socket
    servIP = sys.argv[1]
    servPort = int(sys.argv[2])
    servAdrr = (servIP, servPort)
    bufferSize = 1024
    echo = "abcd"
    bytesSent = str.encode(echo)

    #Variables time
    tmax = 0.0
    tmin = 0.0
    numEnv = 0

    if servPort < 1023:
        print(ERR + "ERR: El nº de puerto debe ser mayor que 1023" + END)
        sys.exit()

    #Creación del socket UDP
    cliSock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    while True:
        try:
            #Envío datos a servidor
            start = time()
            cliSock.sendto(bytesSent, servAdrr)

            #Recibo datos del cliente
            dataRecv = cliSock.recvfrom(bufferSize)
            mss = dataRecv[0]
            add = dataRecv[1]
            t = time() - start
            if t != None:
                tmin, tmax = timeEstad(float(t), tmin, tmax)

            print("-Servidor: %s bytes= %d time= %f" %(add, len(mss),t))
            numEnv += 1
            sleep(1)

        except KeyboardInterrupt:
            print("\n------Estadísticas------\n %i paquetes transmitidos\n tmax= %f tmin= %f tmed= %f\n" %( numEnv, tmax, tmin, (tmax+tmin)/2))
            sys.exit()
