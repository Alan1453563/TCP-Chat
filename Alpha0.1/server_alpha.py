import threading
import socket
import sys

SERVER = '192.168.0.7'
PORT = 5049
FORMAT = 'utf-8'
SIZE = 4096

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER, PORT))

server.listen()
print('Server listening on', SERVER, PORT)

WORDS = ['fuck', 'shit']

AdminsNicknames = ['Admin','Alan','Brian','Ferny']

admins = []
clients = []
nicknames = []

BANS = []

def broadcast(message, c=''):
    msg = message.decode(FORMAT)
    if bad_word(msg):
        print(f'ERROR: {msg} IS A BAD WORD')
        return
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(SIZE)
            message = message.decode(FORMAT)
            message = nicknames[clients.index(client)] +': ' + message
            broadcast(message.encode(FORMAT))
           
            print(message)
            if '/quit' in message:
                nick_index = clients.index(client)
                del admins[nick_index]
                clients.remove(client)
                client.close()
                nickname = nicknames[nick_index]
                print(f'User {nickname} has left.')
                broadcast(f'{nickname} left the chat'.encode(FORMAT))
                nicknames.remove(nickname)
                break
            
            i = clients.index(client)
            if admins[i] and '/' in message:
                try:
                    exc = message.index('/')
                    print('ADMIN USING COMMAND')
                    if message[exc] == '/':
                        print('VALID COMMAND IDENTIFIER')

                        white_index = message.index(' ')
                        user = message[white_index+1:]
                        
                        white_user = user.index(' ')
                        user = user[white_user+1:]

                        if 'kick' in message:
                            print('KICK COMMAND')
                            print(user)
                            
                            if user in nicknames:
                                kick(client, user)
                            else:
                                client.send(f'User {user} not found.'.encode(FORMAT))

                        elif 'unban' in message:
                            print(f'UNBANNING USER {user}')

                            if user in BANS:
                                unban(user)
                            else:
                                client.send(f'User {user} not found'.encode(FORMAT))


                        elif 'ban' in message:
                            print('BAN COMMAND')
                            j = nicknames.index(user)
                            ban_client = clients[j]
                            if ban_client in clients:
                                ban(ban_client, nicknames[j])
                            else:
                                client.send(f'User {user} not found.'.encode(FORMAT))

                    else:
                        client.send('You do not have access to these commands'.encode(FORMAT))
                except:
                    print('We got an error fuck face, commands section')
            else:
                pass
        except:
            nick_index = clients.index(client)
            del admins[nick_index]
            clients.remove(client)
            client.close()
            nickname = nickname[nick_index]
            broadcast(f'{nickname} left the chat'.encode(FORMAT))
            nicknames.remove(nickname)
            break

def handle_server():
    while True:
        message = input('')
        if 'STOP' in message:
            exit()
            
        message = 'SERVER: '+ message
        broadcast(message.encode(FORMAT))
        
def receive():
    thread = threading.Thread(target=handle_server)
    thread.start()
    
    while True:
        client, address = server.accept()
        print(f'Connected with {str(address)}')
        print('BAN method is work in progress')
        print('Client not Banned.')
        client.send('What will be your nickname:'.encode(FORMAT))
        nickname = client.recv(1024).decode(FORMAT)
        
        for i in range(len(BANS)):
            print(i, '. ', BANS[i])
        if nickname in AdminsNicknames:
            admins.append(True)
            nickname = nickname+'*'
        else:
            admins.append(False)
        nicknames.append(nickname)

        if nickname in BANS:
            print('Banned client tried joining')
            client.send('You are banned. Ask an admin to unban you.'.encode(FORMAT))
            client.close()
            return

        clients.append(client)

        print(f'Nickname of the client is {nickname}')
        broadcast(f'{nickname} joined the chat.'.encode(FORMAT))
        client.send('Connected to the server.'.encode(FORMAT))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

def kick(client, name):
    print('USER IN NICKNAMES')
    broadcast(f'{name} has been kicked.'.encode(FORMAT))
    print(f'{name} has been removed')

    index = nicknames.index(name)
    del admins[index]
    kick_user = clients[index]
    kick_user.close()
    nicknames.remove(name)
    clients.remove(kick_user)

def ban(ban_client, name):
    BANS.append(name)
    print(f'BANNING USER {name}')
    
    i = clients.index(ban_client)
    del admins[i]
    clients.remove(ban_client)
    nicknames.remove(name)
    broadcast(f'User {name} has been banned.'.encode(FORMAT))
    ban_client.close()

def unban(name):
    BANS.remove(name)

def bad_word(message):
    for w in WORDS:
        if w in message:
            return True
    return False

def shutdown():
    
    for client in clients:
        client.close()
    nicknames = []    
    
    sys.exit(0)

def server_commands():
    pass

receive()
