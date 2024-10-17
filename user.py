class user:
    def __init__(self, id: int = 0, name: str = "", username: str = "", password: str = "", profile: str = ""):
        self.id = id
        self.name = name
        self.username = username
        self.password = password
        self.profile = profile
    
    def get_id(self):
        return self.id
    
    def get_name(self):
        return self.name
    
    def get_username(self):
        return self.username
    
    def get_password(self):
        return self.password
    
    def get_profile(self):
        return self.profile