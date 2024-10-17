class supplier:
    def __init__(self, id: int = 0, phone: str = "", name: str = "", address: str = "", bank_code: str = ""):
        self.id = id
        self.phone = phone
        self.name = name
        self.address = address
        self.bank_code = bank_code
        
    def get_id(self):
        return self.id
    
    def get_phone(self):
        return self.phone
    
    def get_name(self):
        return self.name
    
    def get_address(self):
        return self.address
    
    def get_bank_code(self):
        return self.bank_code