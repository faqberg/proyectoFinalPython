import socket
import threading
import datetime

def handle_client(clientsocket, address):
    print("Recibo la conexión desde: " + str(address[0]))

    data = clientsocket.recv(1024)
    data_str = data.decode("utf-8")

    log_message = f"{datetime.datetime.now()} - Cliente {address[0]}: {data_str}"
    print(log_message)

    mensaje = b"Conectado"
    clientsocket.send(mensaje)

    clientsocket.close()

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
puerto = 456
print(host)
serversocket.bind((host, puerto))
serversocket.listen(3)

while True:
    clientsocket, address = serversocket.accept()
    client_thread = threading.Thread(target=handle_client, args=(clientsocket, address))
    client_thread.start()