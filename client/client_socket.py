import socket
import select
import sys

IP = 'server'
PORT = 3000
SIZE = 2048

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))

while True:
    socket_list = [sys.stdin, client_socket]
    read_socket, write_socket, error_socket = select.select(socket_list, [], [])

    for socket in read_socket:
        if socket == client_socket:
            message = socket.recv(SIZE)
            print(message.decode('utf-8'))
        else:  # stdin
            message = sys.stdin.readline().rstrip()
            client_socket.send(message.encode())
            UP = '\x1B[1A'
            print(f'{UP}<You> {message}')
