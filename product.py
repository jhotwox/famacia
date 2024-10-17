class product:
    def __init__(
        self,
        id: int = 0,
        name: str = "",
        description: str = "",
        sale_price: float = 0.0,
        purchase_price: float = 0.0,
        discount_sale: int = 0,
        stock: int = 0,
        category: str = "",
        supplier: int = 0
    ):
        self.id = id
        self.name = name
        self.description = description
        self.sale_price = sale_price
        self.purchase_price = purchase_price
        self.discount_sale = discount_sale
        self.stock = stock
        self.category = category
        self.supplier = supplier
    
    def get_id(self):
        return self.id
    
    def get_name(self):
        return self.name
    
    def get_description(self):
        return self.description
    
    def get_sale_price(self):
        return self.sale_price
    
    def get_purchase_price(self):
        return self.purchase_price
    
    def get_discount_sale(self):
        return self.discount_sale
    
    def get_stock(self):
        return self.stock
    
    def get_category(self):
        return self.category
    
    def get_supplier(self):
        return self.supplier
    
    def float_discount(self):
        return self.discount_sale / 100