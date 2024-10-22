from customtkinter import CTk, CTkButton as Button, DISABLED, CTkFrame as Frame, CTkLabel as Label
from user import user as user_class
# from users import Users
# from customers import Customers

class Menu(Frame):
    def __init__(self, container, controller, profile: user_class, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        
        self.controller = controller
        self.profile = profile
        self.lbTitle = Label(self, text=f"Hola {profile.get_name()} 👋", font=("Calisto MT", 36, "bold"))
        self.lbTitle.grid(row=0, column=0, pady=20, columnspan=2)
        
        self.bt_users = Button(self, text="Usuarios", command=self.open_users)
        self.bt_users.grid(row=1, column=0, padx=10, pady=10)
        
        self.bt_customers = Button(self, text="Clientes", command= self.open_customers)
        self.bt_customers.grid(row=1, column=1, padx=10, pady=10)
        
        self.bt_products = Button(self, text="Almacen", command=self.open_products)
        self.bt_products.grid(row=2, column=0, padx=10, pady=10)
        
        self.bt_purchases = Button(self, text="Compras", command=self.open_purchases)
        self.bt_purchases.grid(row=2, column=1, padx=10, pady=10)
        
        self.bt_new_sale = Button(self, text="Nueva venta", command=self.open_new_sale)
        self.bt_new_sale.grid(row=3, column=0, padx=10, pady=10)
        
        self.bt_sales = Button(self, text="Ventas", command=self.open_sales)
        self.bt_sales.grid(row=3, column=1, padx=10, pady=10)
        
        self.bt_suppliers = Button(self, text="Proveedores", command=self.open_suppliers)
        self.bt_suppliers.grid(row=4, column=0, padx=10, pady=10)
        
        self.btExit = Button(self, text="Salir", command=self.exit)
        self.btExit.grid(row=4, column=1, padx=10, pady=10)
        
        if profile.get_profile() == "secretaria":
            self.bt_users.configure(state=DISABLED)
            self.bt_purchases.configure(state=DISABLED)
            self.bt_new_sale.configure(state=DISABLED)
        
        if profile.get_profile() == "mecanico":
            self.bt_users.configure(state=DISABLED)
            self.bt_customers.configure(state=DISABLED)
            self.bt_new_sale.configure(state=DISABLED)
    
    def open_users(self) -> None:
        self.controller.show_frame("Users") 
    
    def open_customers(self) -> None:
        self.controller.show_frame("Customers")

    def open_products(self) -> None:
        self.controller.show_frame("Products")
    
    def open_purchases(self) -> None:
        self.controller.show_frame("Purchases")

    def open_new_sale(self) -> None:
        self.controller.show_frame("Sales")
        
    def open_sales(self) -> None:
        self.controller.show_frame("Table")
        return 
        
    def open_suppliers(self) -> None:
        self.controller.show_frame("Suppliers")
        
    def exit(self) -> None:
        if hasattr(self.controller, "show_frame"):
            self.controller.show_frame("Login")
        else:
            print("[-] Error con el controlador")