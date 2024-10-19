class sale:
    def __init__(self, id: int = 0, customer_id: int = 0, total: float = 0.0, date: str = "", discount: float = 0.0) -> None:
        self.id = id
        self.customer_id = customer_id
        self.total = total
        self.date = date
        self.discount = discount
        
    def get_id(self):
        return self.id
    
    def get_customer_id(self):
        return self.customer_id
    
    def get_total(self):
        return self.total
    
    def get_date(self):
        return self.date
    
    def get_discount(self):
        return self.discount
        