import socket
from _thread import *

IP = ''
POST = 3000
SIZE = 2048
client_list = []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((IP, POST))
server_socket.listen(100)

def client_thread(cilent, addr):
    cilent.send('Welcome to this chatroom!'.encode())
    while True:
        try:
            message = cilent.recv(SIZE)
            if message:
                message_to_send = '<' + addr[0] + '> ' + message.decode('utf-8')
                print(message_to_send)
                broadcast(message_to_send, cilent)
            else:
                remove(cilent)
        except:
            continue

def broadcast(message, sender):
	for client in client_list:
		if client != sender:
			try:
				client.send(message.encode())
			except:
				remove(client)

def remove(client):
    if client in client_list:
        client_list.remove(client)
        client.close()

while True:
	client_socket, client_addr = server_socket.accept()
	client_list.append(client_socket)
	print(client_addr[0] + ' connected')
	start_new_thread(client_thread, (client_socket, client_addr))
