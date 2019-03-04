# Simple-Socket-Chat
Using python

Program sederhana untuk chatting dan transfer file

## Fungsionalitas
Program ini harus bisa:
- [x] Mengirim pesan biasa dan di broadcast ke semua clients
- [x] Bisa mengirim file dengan perintah SEND minimal 3MB 

### HASIL
1. Mengirim pesan biasa berhasil
![hasil1](/images/hasil1.png)
2. Berhasil mengirim file dengan nama _See-Saw.mp3_ (11.5MB) dan muncul pada client2 dengan nama _terima_See-Saw.mp3_. Client 1 dan 2 juga masih bisa saling berkomunikasi tanpa ada error.
![commandsend](/images/commandsend.png)
![hasilclient2](/images/hasilclient2.png)
![masihbisa](/images/masihbisa.png)

## Penjelasan Code

### Server (chat.py)
```python
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
```

Pertama server akan menerima pesan dari client. Pesan jika pesan ada isinya maka akan dilanjutkan ke tahap berikutnya namun jika tidak maka data client akan dihapus dari list_of_clients.

Pada tahap selanjutnya pesan akan dibedakan menjadi 2 yaitu pesan dengan kata **SEND** didalamnya dan pesan tanpa SEND.

Pesan dengan SEND akan menerima pesan yang pertama yaitu adalah pesan yang berisi commandnya. Dari pesan tersebut akan diambil nama filenya lalu dibuka dan diisi dengan data yang diterima berikutnya yaitu data file yang dikirim. Kami menggunakan wb karena data yang server terima berupa tulisan binary. Server akan mencari string **//AGUEL//TAMTAM//** jika ada string tersebut artinya file sudah terkirim semua dan berikutnya keluar dari while. Semua pesan yang diterima oleh server akan dikirimkan kembali ke client-client untuk dibuat filenya pada masing-masing client.

Pesan yang tidak memiliki send akan dikirim langsung ke semua client karena hanya berupa pesan biasa.

### Client (chatclient.py)
```python
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
```

Pada clients socket dibagi menjadi 2 hal yaitu socket yang mengirim dan socket yang menerima pesan. Pada socks yang menerima pesan, pesan akan dibagi jadi 2 sama seperti pada server yaitu pesan dengan SEND dan tanpa SEND. Pesan tanpa SEND akan langsung di print dan pesan dengan SEND akan diproses untuk dibuat filenya. Algoritma yang digunakan ketika pembentukan file adalah sama dengan yang ada di server.

Pada socks yang mengirim pesan juga dibagi jadi 2 yaitu pesan dengan SEND dan tanpa SEND. Pesan dengan send akan dibaca ngan rb (secara binary) dan dikirim perline ke server. Jika sudah selesai maka akan diakhiri dengan string *//AGUEL//TAMTAM//* dan dikirimkan ke server agar server tahu bahwa proses pengiriman telah selesai. Sedangkan pesan tanpa SEND akan langsung dikirimkan secara langsung ke server.