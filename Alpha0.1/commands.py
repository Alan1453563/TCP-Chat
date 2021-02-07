'''
    /help:  Show available commands
    /kick:  kick a user
    /ban:   Ban a user
    /mute:  mute a user
    /startGame: Start a vote for a speedtype game
    /censorChat: Censor Profanity
    /quit
    For any more questions contact the owners of the repository
'''
from user import Client

class Command:
    def __init__(self):
        self.user = None
                
    def executeCommand(self, cmd, user):
        self.user = user
        
    def help(self):
        pass
    
    def kick(self):
        if not user.isAdmin:
            user.send('You do not have the privileges to perform this command'.encode('utf-8'))
            pass
        
        
    def ban(self):
        pass
        
    def mute(self):
        pass
        
    def voteGame(self):
        pass
    
    def censorChat(self):
        pass