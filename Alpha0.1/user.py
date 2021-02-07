
class Client:
    def __init__(self, chat_name, client, admin_names):
        self.name = chat_name
        self.client = client
        self.isAdmin = False
        self.friends = []
        self.ban = False
        
        convert_to_admin(self.name, admin_names)
        
    def connect(self, c):
        pass
        
    def send_msg(self):
        pass
        
    def convert_to_admin(self,admin_names):
        if self.name in admin_names:
            isAdmin = True
            return
        