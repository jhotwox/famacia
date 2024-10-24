from customtkinter import CTkButton as Button, CTkEntry as Entry, CTkLabel as Label, CTkFrame as Frame
from tkinter import messagebox
from functions import is_empty
from db_user import db_user
from user import user as user_class

class Login_Manager(Frame):
    def __init__(self, container, controller, profile: user_class, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        
        self.container = container
        self.controller = controller
        
        lbTitle = Label(self, text="DAR ACCESO", font=("Calisto MT", 36, "bold"))
        lbTitle.grid(row=0, column=0, pady=20, columnspan=2)
        
        self.txUsername = Entry(self, width=200, placeholder_text="Username")
        self.txUsername.grid(row=1, column=0, padx=20, pady=10, columnspan=2)
        self.txUsername.insert(0, "cristian")
        
        self.txPass = Entry(self, width=200, placeholder_text="Contraseña", show="*")
        self.txPass.grid(row=2, column=0, padx=20, pady=10, columnspan=2)
        self.txPass.insert(0, "123456")
        
        self.bt_return = Button(self, text="Regresar", command=lambda: self.controller.show_frame("Sales"))
        self.bt_return.grid(row=3, column=0, padx=10)
        self.btLogin = Button(self, text="Ingresar", command=self.login)
        self.btLogin.grid(row=3, column=1, padx=10)
    
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
        self.user = db_user.authenticate_manager(self, aux)
        
        if self.user is not None:
            self.controller.shared_data["VALIDATE"] = True
            self.txUsername.delete(0, "end")
            self.txPass.delete(0, "end")
            self.controller.show_frame("Sales")