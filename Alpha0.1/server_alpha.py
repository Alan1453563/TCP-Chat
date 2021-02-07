import threading
import socket
import sys

from user import Client
from commands import Command

SERVER = '192.168.0.7'
PORT = 5049
FORMAT = 'utf-8'
SIZE = 4096

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((SERVER, PORT))

server.listen()
print('Server listening on', SERVER, PORT)

WORDS = ['oof']

AdminsNicknames = ['Admin','Alan','Brian','Ferny']

admins = []
clients = []
nicknames = []

users = []

BANS = []

'''
Sends a message by passing a String(message)
'''
def broadcast(message, c=''):
    msg = message.decode(FORMAT)
    bad, msg = bad_word(msg)
    if bad:
        print(f'ERROR: {msg} CONTAINS A BAD WORD')
        message = msg.encode(FORMAT)
    for client in clients:
        client.send(message)

#CLEAN UP
def handle(client):
    while True:
        try:
            message = client.recv(SIZE)
            message = message.decode(FORMAT)
            if message[0] == '/':
                Command()
            
            message = nicknames[clients.index(client)] +': ' + message
            broadcast(message.encode(FORMAT))
           
            print(message)
        
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
            print('Wegot here before method')
            shutdown()
            
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

'''
Sensors the bad word with '*', and returns that as a string
    EX.
        fuck you --> **** you
'''
def bad_word(message): 
    for w in range(len(WORDS)):
        if WORDS[w] in message:
            
            L = list(message.split(' '))
            msg_bad = L.index(WORDS[w])
            
            censored = len(L[msg_bad])*'*'

            L.remove(L[msg_bad])
            L.insert(msg_bad, censored)
            message = ' '.join(L)
            
            return True, message
    
    return False, message

def shutdown():
    print('Closing clients')
    for client in clients:
        client.close()
    nicknames = []    
    
    sys.exit(0)

'''
Ferny for the help_method I want you to print the list of commands available to the server
In this program to print instead of using "print('')", you use the following:
         
         TO SEND TO ALL USERS:
         broadcast(message.encode(FORMAT))
         
         TO SEND TO ONE USER:
         client.send(message.encode(FORMAT))
         
The list of commands are the following:
    /help
    /kick
    /ban
    /mute
    /startGame
    /censorChat
    
An Example:

The user would type:
    /help
    
Then the following would print ONLY on his screen:

    /help:  Show available commands
    /kick:  kick a user
    /ban:   Ban a user
    /mute:  mute a user
    /startGame: Start a vote for a speedtype game
    /censorChat: Censor Profanity
    For any more questions contact the owners of the repository

You're gonna write your code under help_method underneath this comment,
MAKE SURE TO DELETE pass

Ferny if you have any questions let me know.  
'''
def help_method():
    pass


receive()