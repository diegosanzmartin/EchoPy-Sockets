import socket           #Funciones orientadas a conexión
import sys              #Funciones sistema
from time import time   #Cronometrar tiempos

def timeEstad(t, tmin, tmax): #Esta función compara los tiempos para
    if tmax == 0.0 and tmin == 0.0: #determinar cual es el tmin y el tmax
        return t, t
    elif t > tmax:
        return tmin, t
    elif t < tmin:
        return t, tmax
    else:
        return tmin, tmax

if __name__ == "__main__":
    if len(sys.argv) != 3:  #Comprobamos el nº de argumentos
        print('Error: El numero de argumentos no es valido\n')
        sys.exit()

    #Variables socket
    servIP = sys.argv[1]
    servPort = int(sys.argv[2])
    server_address = (servIP, servPort)
    numEnv = 0

    #Variables del tiempo
    tmax = 0.0
    tmin = 0.0
    tmed = 0.0

    if servPort < 1023: #Comprobamos el nº de puerto
        print('Error: El numero de puerto tiene que ser mayor que 1023\n')
        sys.exit()

    #Creación del socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Conexión socket
    sock.connect(server_address)

    while(True): #Bucle infinito
        try:
            start = time() #Empieza el "cronómetro"
            message = 'Hola\n'
            bytesSent = sock.send(message.encode())

            received = 0
            expected = len(message)

            while received < expected: #Mientras no se haya enviado todo el mensaje
                data = sock.recv(1024)
                received += len(data)
            
                t = time() - start      #Tiempo en realizar las conexiones
                if t != None:
                    tmin, tmax = timeEstad(float(t), tmin, tmax)

                print("-Servidor: %s bytes = %d: time = %f" %(server_address, bytesSent, t))
                numEnv += 1

        except KeyboardInterrupt:
            #Cerramos el sicket TCP
            sock.close()
            #Al terminar el bucle (CTRL-C) mostramos las estadísticas del ping
            print("\n------Estadísticas------\n %i paquetes transmitidos\n tmax= %f tmin= %f tmed= %f\n" %( numEnv, tmax, tmin, (tmax+tmin)/2))
            sys.exit()