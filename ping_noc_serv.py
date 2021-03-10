import signal, socket, sys, os      #Funciones orientadas a conexión, sistema
from time import time               #Cronometrar tiempos
from time import sleep

def timeEstad(t, tmin, tmax):       #Esta función compara los tiempos para
    if tmax == 0.0 and tmin == 0.0:    #determinar cual es el tmin y el tmax
        return t, t
    elif t > tmax:
        return tmin, t
    elif t < tmin:
        return t, tmax
    else:
        return tmin, tmax


if __name__ == "__main__":          
    if len(sys.argv) != 2 :         #Esta función compara los tiempos para
        print(ERR + "ERR: Nº de argumentos no válidos" + END)
        sys.exit()
    
    #Variables socket
    servIP = "127.0.0.1"
    servPort = int(sys.argv[1])
    bufferSize = 1024

    #Variables tiempo
    tmax = 0.0
    tmin = 0.0
    numEnv = 0

    if servPort < 1023:             #Comprobamos el nº de puerto
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
            start = time()          #Iniciamos el "cronómetro"
            mss = dataRecv[0]       #Obtenemos de dataRecv el mensaje
            add = dataRecv[1]       #Obtenemos de dataRecv la direcc del cli

            #Envío respuesta a cliente
            servSock.sendto(mss, add)
            t = time() - start      #Tiempo en realizar las conexiones
            if t != None:
                tmin, tmax = timeEstad(float(t), tmin, tmax)    #Obtenemos los tiempos tmax y tmin

            print("-Cliente: %s bytes= %d time= %f" %(add, len(mss),t))
            numEnv += 1             #Incremento del nº de paquetes
            sleep(1)

        except KeyboardInterrupt:
            #Calculamos el tiempo en realizar las conexiones
            print("\n------Estadísticas------\n %i paquetes transmitidos\n tmax= %f tmin= %f tmed= %f\n" %( numEnv, tmax, tmin, (tmax+tmin)/2))
            sys.exit()