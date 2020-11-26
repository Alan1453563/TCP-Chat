import threading
import socket

SERVER = '192.168.0.7'
PORT = 5048
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER, PORT))

server.listen()
print('Server listening on', SERVER,':', PORT)

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remoce(client)
            client.close()
            nickname = nickname[index]
            broadcast(f'{nickname} left the chat'.encode(FORMAT))
            nicknames.remove(nickname)
            break

def receive():
    while True:
        client, address = server.accept()
        print(f'Connected with {str(address)}')

        client.send('What will be your nickname:'.encode(FORMAT))
        nickname = client.recv(1024).decode(FORMAT)
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of the client is {nickname}')
        broadcast(f'{nickname} joined the chat.'encode(FORMAT))
        client.send('Connected to the server.'.encode(FORMAT))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()


