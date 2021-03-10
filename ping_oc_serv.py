import socket                    #Funciones orientadas a conexión
import sys                       #Funciones sistema
from time import time            #Cronometrar tiempos
from time import sleep

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
    if len(sys.argv) != 2:      #Comprobamos el nº de argumentos
        print('Error: El numero de argumentos no es valido\n')
        sys.exit()

    #Variables socket
    servPort = int(sys.argv[1])
    servIP = "127.0.0.1"
    serv_addr = (servIP, servPort)
    numEnv = 0

    #Variables del tiempo
    tmax = 0.0
    tmin = 0.0
    tmed = 0.0

    if servPort < 1023:           #Comprobamos el nº de puertos
        print('Error: El numero de puerto tiene que ser mayor que 1023\n')
        sys.exit()

    #Creación del socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Conexión socket
    sock.bind(serv_addr)

    sock.listen(1) #El socket está a la escucha del cliente

    connection, client_addr = sock.accept()

    while(True): #Bucle infinito
        try:
            start = time() #Empieza el "cronómetro"
            dataRecv = connection.recvfrom(20)
            mss = dataRecv[0]

            connection.send(mss)
            t = time() - start
            if t != None:
                tmin, tmax = timeEstad(float(t), tmin, tmax)

            print("-Cliente: %s bytes= %d time= %f" %(client_addr, len(mss),t))
            numEnv += 1 #incremento del nº de paquetes
            sleep(1) #Se suspende la ejecucción del programa durante 1s

        except KeyboardInterrupt:
            #Cerramos el sicket TCP
            sock.close()
            #Al terminar el bucle (CTRL-C) mostramos las estadísticas del ping
            print("\n------Estadísticas------\n %i paquetes transmitidos\n tmax= %f tmin= %f tmed= %f\n" %( numEnv, tmax, tmin, (tmax+tmin)/2))
            sys.exit()