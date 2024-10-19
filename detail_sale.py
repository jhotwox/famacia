class detail_sale:
    def __init__(self, sale_id: int = 0, product_id: int = 0, quantity: int = 0, unitary_price: float = 0.0) -> None:
        self.sale_id = sale_id
        self.product_id = product_id
        self.quantity = quantity
        self.unitary_price = unitary_price
        
    def get_sale_id(self):
        return self.sale_id
    
    def get_product_id(self):
        return self.product_id
    
    def get_quantity(self):
        return self.quantity
    
    def get_unitary_price(self):
        return self.unitary_price
        