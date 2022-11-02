import socket
import select
import sys
import time

IP = 'server'
PORT = 3000
SIZE = 2048

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
message = client_socket.recv(SIZE)
print(message.decode('utf-8'))

while True:
    socket_list = [client_socket, sys.stdin]
    read_socket, write_socket, error_socket = select.select(socket_list, [], [])

    for socket in read_socket:
        time.sleep(1)  # This line only need for testing docker compose
        if socket == client_socket:
            message = socket.recv(SIZE)
            print(message.decode('utf-8'))
        else:  # stdin
            message = sys.stdin.readline().rstrip()

            if message == '':
                exit()
            if message == '/wait':  # wait for socket receive
                message = client_socket.recv(SIZE)
                print(message.decode('utf-8'))
                continue
            
            client_socket.send(message.encode())
            print('<You> ' + message)
