import socket
import threading
import sys

SERVER = '192.168.0.5'
PORT = 5049
FORMAT = 'utf-8'

nickname = input('Choose a nickname: ')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))

def receive():
    while True:
        try:
            message = client.recv(1024).decode(FORMAT)
            if message == 'What will be your nickname:':
                client.send(nickname.encode(FORMAT))
            else:
                print(message)
        except:
            print('An error occurred')
            client.close()
            break

def write():
    while True:
        message = input('')
        client.send(message.encode(FORMAT))
        if message == '/quit':
            quit()

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()

