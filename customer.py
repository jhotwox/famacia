class customer:
    def __init__(self, id: int = 0, points: int = 0, name: str = "", phone: str = "", adress: str = ""):
        self.id = id
        self.points = points
        self.name = name
        self.phone = phone
        self.adress = adress
    
    def get_id(self):
        return self.id
    
    def get_points(self):
        return self.points
    
    def get_name(self):
        return self.name
    
    def get_phone(self):
        return self.phone
    
    def get_adress(self):
        return self.adress