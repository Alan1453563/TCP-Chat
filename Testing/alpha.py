import threading
import socket
import sys
#Testing variables

FORMAT = 'utf-8'
SIZE = 4096
WORDS = ['test']


'''
Add methods to test before running on server
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

def broadcast(message, c=''):
    msg = message
    bad, msg = bad_word(msg)
    if bad:
        print(f'ERROR: {msg} IS A BAD WORD')
        message = msg
    print(msg)
        
        
if __name__ == '__main__':
    
    while True:
        broadcast(input(''))