import signal, socket, sys, os      #Funciones orientadas a conexión, sistema
from time import time               #Cronometrar tiempos
from time import sleep

ERR = "\033[93m"
END = "\033[0m"

def timeEstad(t, tmin, tmax):       #Esta función compara los tiempos para
    if tmax == 0.0 and tmin == 0.0: #determinar cual es el tmin y el tmax
        return t, t
    elif t > tmax:
        return tmin, t
    elif t < tmin:
        return t, tmax
    else:
        return tmin, tmax


if __name__ == "__main__":
    if len(sys.argv) != 3 :         #Comprobamos el nº de argumentos
        print(ERR + "ERR: Nº de argumentos no válidos" + END)
        sys.exit()
    
    #Variables socket
    servIP = sys.argv[1]
    servPort = int(sys.argv[2])
    servAdrr = (servIP, servPort)
    bufferSize = 1024
    echo = "abcd"
    bytesSent = str.encode(echo)

    #Variables tiempo
    tmax = 0.0
    tmin = 0.0
    numEnv = 0

    if servPort < 1023:             #Comprobamos el nº de puerto
        print(ERR + "ERR: El nº de puerto debe ser mayor que 1023" + END)
        sys.exit()

    #Creación del socket UDP
    cliSock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    while True:
        try:
            #Envío datos a servidor
            start = time()          #Iniciamos el "cronómetro"
            cliSock.sendto(bytesSent, servAdrr)

            #Recibo datos del cliente
            dataRecv = cliSock.recvfrom(bufferSize)
            mss = dataRecv[0]       #Obtenemos de dataRecv el mensaje
            add = dataRecv[1]       #Obtenemos de dataRecv la direcc del cli

            t = time() - start      #Tiempo en realizar las conexiones
            if t != None:
                tmin, tmax = timeEstad(float(t), tmin, tmax)    #Obtenemos los tiempos tmax y tmin

            print("-Servidor: %s bytes= %d time= %f" %(add, len(mss),t))
            numEnv += 1             #Incremento del nº de paquetes
            
        except KeyboardInterrupt:
            #Al terminar el bucle (CTRL-C) mostramos las estadísticas del ping
            print("\n------Estadísticas------\n %i paquetes transmitidos\n tmax= %f tmin= %f tmed= %f\n" %( numEnv, tmax, tmin, (tmax+tmin)/2))
            sys.exit()
