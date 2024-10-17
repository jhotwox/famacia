from customtkinter import CTkFrame as Frame, CTkScrollbar as Scrollbar
from user import user as user_class
from tkinter.ttk import Treeview
from table_style import apply_style

class Table(Frame):
    def __init__(self, container, controller, profile: user_class, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        
        self.controller = controller
        
        frame = Frame(self)
        frame.grid(row=0, column=0, sticky="nsew")
        
        scroll_y = Scrollbar(frame)
        scroll_y.grid(row=0, column=1, sticky="ns") #Desplazamiento vertical
        
        scroll_x = Scrollbar(frame, orientation="horizontal")
        scroll_x.grid(row=1, column=0, sticky="ew") #Desplazamiento horizontal
        
        apply_style()
        self.table = Treeview(
            frame,
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
            style="Custom.Treeview"
        )
        self.table.grid(row=0, column=0, sticky="nsew")
        
        scroll_y.configure(command=self.table.yview)
        scroll_x.configure(command=self.table.xview)
        
        self.table['columns'] = ("ID", "Nombre", "Username", "Perfil")
        self.table.column("#0", width=0, stretch=False)
        self.table.column("ID", anchor="center", width=50)
        self.table.column("Nombre", anchor="center", width=150)
        self.table.column("Username", anchor="center", width=150)
        self.table.column("Perfil", anchor="center", width=150)
        
        self.table.heading("#0", text="", anchor="center")
        self.table.heading("ID", text="ID", anchor="center")
        self.table.heading("Nombre", text="Nombre", anchor="center")
        self.table.heading("Username", text="Username", anchor="center")
        self.table.heading("Perfil", text="Perfil", anchor="center")
        
        # self.table.grid(row=0, column=0, sticky="nsew")
        
        self.insert([
            ["1", "Cristian", "cristian", "admin"],
            ["2", "Juan", "juan", "secretaria"],
            ["3", "Pedro", "pedro", "mecanico"],
            ["4", "Maria", "maria", "gerente"],
            ["5", "Carlos", "carlos", "cajero"],
            ["6", "Jose", "jose", "admin"],
            ["7", "Andres", "andres", "secretaria"],
            ["1", "Cristian", "cristian", "admin"],
            ["2", "Juan", "juan", "secretaria"],
            ["3", "Pedro", "pedro", "mecanico"],
            ["4", "Maria", "maria", "gerente"],
            ["5", "Carlos", "carlos", "cajero"],
            ["6", "Jose", "jose", "admin"],
            ["7", "Andres", "andres", "secretaria"]
        ])
        
    def insert(self, data: list) -> None:
        for i, row in enumerate(data):
            self.table.insert("", "end", iid=i, values=row)
    