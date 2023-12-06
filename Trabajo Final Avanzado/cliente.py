import socket
import sys

try:
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "192.168.1.36"
    puerto = 456
    clientsocket.connect((host, puerto))

    # Enviar datos al servidor
    mensaje = "Hola, servidor. Este es mi mensaje."
    clientsocket.send(mensaje.encode("utf-8"))

    # Recibir respuesta del servidor
    respuesta = clientsocket.recv(1024)
    print(respuesta.decode('utf-8'))

    # Cerrar la conexión
    clientsocket.close()

except socket.error as e:
    print(f"Error en la conexión: {e}")
    sys.exit(1)