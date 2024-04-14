import socket
import psutil
import time
import json

HOST = '127.0.0.1'
PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((HOST, PORT))

while True:
    cpu_percent = psutil.cpu_percent(interval=1)

    total_ram_gb = psutil.virtual_memory().total / (1024 ** 3)
    available_ram_gb = psutil.virtual_memory().available / (1024 ** 3)

    data = {
        "cpu_usage": cpu_percent,
        "ram_available": available_ram_gb
    }

    data_json = json.dumps(data)

    # response = client_socket.recv(1024).decode()

    # if response:
    #     print("Message from server:", response)

    client_socket.sendall(data_json.encode())

    time.sleep(1)
