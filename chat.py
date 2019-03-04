import socket
import select
import sys
from thread import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

IP_address = "127.0.0.1"

Port = 8081

server.bind((IP_address, Port))

server.listen(100)

list_of_clients = []

def clientthread(conn, addr):
	while True:
		try:
			message = conn.recv(2048)
			if message:
				if "SEND" in message:
					messagex = message.split('\n')
					broadcast(messagex[0],conn)

					messages = message.split(' ')

					messages = messages[1].split('\n')
					with open("terima_"+messages[0], 'wb') as file:
					    while True:
					        data = conn.recv(2048)
					        if '//AGUEL//TAMTAM//' in data:
					        	broadcast("//AGUEL//TAMTAM//",conn)
					        	break
					        file.write(data)
					        broadcast(data, conn)

				else:
					messages = message.split('\n')
					print "<" + addr[0] + "> " + messages[0]

					message_to_send = "<" + addr[0] + "> " + messages[0]
					broadcast(message_to_send, conn)
			else:
				remove(conn)
		except:
			continue

def broadcast(message, connection):
	for clients in list_of_clients:
		if clients!=connection:
			try:
				clients.send(message)
			except:
				clients.close()
				remove(clients)

def remove(connection):
	if connection in list_of_clients:
		list_of_clients.remove(connection)

while True:
	conn, addr = server.accept()
	list_of_clients.append(conn)
	print addr[0] + " connected"
	start_new_thread(clientthread,(conn,addr))

conn.close()
server.close()