import socket
import json

# TODO: get these values from .env
HOST = '127.0.0.1'
PORT = 12345
CPU_THRESHOLD = 80
RAM_THRESHOLD = 0.5

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))

server_socket.listen(5)

print("Server listening on", HOST, "port", PORT)

client_socket, client_address = server_socket.accept()

print("Connected to client:", client_address)

while True:
    data = client_socket.recv(1024).decode()

    if not data:
        break

    data_json = json.loads(data)

    print("Received data from client")

    cpu_usage = data_json["cpu_usage"]
    available_ram = data_json["ram_available"]
    print(cpu_usage)
    print(available_ram)

    if cpu_usage > CPU_THRESHOLD:
        client_socket.sendall("High CPU usage detected!".encode())
    
    if available_ram < RAM_THRESHOLD:
        client_socket.sendall("Low available RAM detected!".encode())

client_socket.close()
