class detail_purchase:
    def __init__(self, purchase_id: int = 0, product_id: int = 0, unitary_price: float = 0.0, quantity: int = 0) -> None:
        self.purchase_id = purchase_id
        self.product_id = product_id
        self.unitary_price = unitary_price
        self.quantity = quantity
        
    def get_purchase_id(self) -> int:
        return self.purchase_id
    
    def get_product_id(self) -> int:
        return self.product_id
    
    def get_unitary_price(self) -> float:
        return self.unitary_price
    
    def get_quantity(self) -> int:
        return self.quantity
