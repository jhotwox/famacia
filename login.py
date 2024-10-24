from customtkinter import CTkButton as Button, CTkEntry as Entry, CTkLabel as Label, CTk, CTkFrame as Frame
from tkinter import messagebox
from functions import is_empty
from db_user import db_user
from user import user as user_class
from menu import Menu
from users import Users
from customers import Customers
from suppliers import Suppliers
from products import Products
from purchases import Purchases
from sales import Sales
from login_manager import Login_Manager

class Login(Frame):
    def __init__(self, container, controller, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        
        # self.self = self
        self.container = container
        self.controller = controller
        
        lbTitle = Label(self, text="Login", font=("Calisto MT", 36, "bold"))
        lbTitle.grid(row=0, column=1, pady=20)

        # self.lbUsername = Label(self, text="Username", font=("Calisto MT", 16))
        # self.lbUsername.grid(row=1, column=0)
        self.txUsername = Entry(self, width=200, placeholder_text="Username")
        self.txUsername.grid(row=1, column=1, padx=20, pady=10)
        self.txUsername.insert(0, "cristian")
        
        # self.lbPass = Label(self, text="Contraseña", font=("Calisto MT", 16))
        # self.lbPass.grid(row=2, column=0, pady=10)
        self.txPass = Entry(self, width=200, placeholder_text="Contraseña", show="*")
        self.txPass.grid(row=2, column=1, padx=20, pady=10)
        self.txPass.insert(0, "123456")
        
        self.btLogin = Button(self, text="Ingresar", command=self.login)
        self.btLogin.grid(row=3, column=1, pady=15)
    
    def validate(self) -> bool:
        username = self.txUsername.get()
        password = self.txPass.get()
        
        if is_empty(username):
            messagebox.showwarning("Campo vacio", "El campo username no debe de estar vacio")
            return False
        if is_empty(password):
            messagebox.showwarning("Campo vacio", "El campo contraseña no debe de estar vacio")
            return False
        if len(password) < 6:
            messagebox.showwarning("Invalido", "La contraseña es demasiado corta")
            return False
        return True

    def login(self) -> None:
        username = self.txUsername.get()
        password = self.txPass.get()
        
        if not self.validate():
            return
        
        aux = user_class(username=username, password=password)
        self.user = db_user.authenticate(self, aux)
        
        if self.user.get_profile() == "admin":
            windows = {
                "Menu": Menu,
                "Users": Users,
                "Customers": Customers,
                "Suppliers": Suppliers,
                "Products": Products,
                "Purchases": Purchases,
                "Sales": Sales
            }
        if self.user.get_profile() == "gerente":
            windows = {
                "Menu": Menu,
                "Customers": Customers,
                "Sales": Sales
            }
        if self.user.get_profile() == "cajero":
            windows = {
                "Menu": Menu,
                "Sales": Sales,
                "Login_Manager": Login_Manager
            }
        
        # Recorrer las clases
        for key, F in windows.items():
            # La llave se vuelve la clase
            self.controller.add_frame(key, F, self.user)

        self.controller.show_frame("Menu")