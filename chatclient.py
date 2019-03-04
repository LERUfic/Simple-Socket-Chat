import socket
import select
import sys

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP_address = "127.0.0.1"

Port = 8081

server.connect((IP_address, Port))

while True:
	sockets_list = [sys.stdin, server]
	read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])

	for socks in read_sockets:
		if socks == server:
			message = socks.recv(2048)
			if message:
				if "SEND" not in message:
					print message
				if "SEND" in message:
					messages = message.split(' ')
					messages = messages[1].split('\n')
					with open("terima_"+messages[0], 'wb') as file:
					    while True:
					        data = socks.recv(2048)
					        if '//AGUEL//TAMTAM//' in data:
					        	break
					        file.write(data)
		else:
			message = sys.stdin.readline()
			if "SEND" in message:
				server.send(message)
				messages = message.split(' ')
				messages = messages[1].split('\n')
				file = open(messages[0],'rb')
				line = file.read(2048)
				while(line):
					server.send(line)
					line = file.read(2048)
				file.close()
				server.send("//AGUEL//TAMTAM//")

			else:
				server.send(message)
				sys.stdout.write("<You> ")
				sys.stdout.write(message)
				sys.stdout.flush()

server.close()