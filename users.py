from customtkinter import END, CTkButton as Button, CTkEntry as Entry, CTkLabel as Label, DISABLED, NORMAL as ENABLE, CTkFrame as Frame, CTkOptionMenu as OptMenu, StringVar, CTkScrollbar as Scrollbar
from tkinter import messagebox
from tkinter.ttk import Treeview
from functions import entry_empty, is_alphabetic
from db_user import db_user
from user import user as user_class
from table_style import apply_style
from db_functions import name_available

class Users(Frame):
    def __init__(self, container, controller, profile: user_class, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        
        self.controller = controller
        self.band = None
        
        fr_search = Frame(self)
        fr_search.grid(row=0, column=0, sticky="nsw", padx=10, pady=10)
        fr_entry = Frame(self)
        fr_entry.grid(row=1, column=0, sticky="nsw", padx=10, pady=10)
        fr_table = Frame(self)
        fr_table.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        fr_button = Frame(self)
        fr_button.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)
        
        self.lb_search = Label(fr_search, text="ID a buscar: ", font=("Calisto MT", 12))
        self.lb_search.grid(row=0, column=0, padx=5)
        self.tx_search = Entry(fr_search, placeholder_text="ID a buscar", width=200)
        self.tx_search.grid(row=0, column=1,  padx=10, pady=10)
        self.bt_search = Button(fr_search, text="Buscar", border_width=2, width=100, command=self.search_user)
        self.bt_search.grid(row=0, column=2, padx=5, pady=10)

        self.lb_id = Label(fr_entry, text="ID")
        self.lb_id.grid(row=0, column=0, pady=0, sticky="w")
        self.tx_id = Entry(fr_entry, placeholder_text="ID")
        self.tx_id.grid(row=0, column=1, pady=5)

        self.lb_name = Label(fr_entry, text="Nombre")
        self.lb_name.grid(row=1, column=0, pady=0, sticky="w")
        self.tx_name = Entry(fr_entry, placeholder_text="Nombre")
        self.tx_name.grid(row=1, column=1, pady=5, padx=20)
        self.lb_username = Label(fr_entry, text="Username")
        self.lb_username.grid(row=1, column=2, pady=0, sticky="w")
        self.tx_username = Entry(fr_entry, placeholder_text="Username")
        self.tx_username.grid(row=1, column=3, pady=5, padx=20)

        self.lb_password = Label(fr_entry, text="Contraseña")
        self.lb_password.grid(row=2, column=0, pady=0, sticky="w")
        self.tx_password = Entry(fr_entry, placeholder_text="Contraseña")
        self.tx_password.grid(row=2, column=1, pady=5, padx=20)
        
        self.lb_profile = Label(fr_entry, text="Perfil")
        self.lb_profile.grid(row=2, column=2, pady=0, sticky="w")
        self.selected_profile = StringVar(value="admin")
        self.opm_profile = OptMenu(fr_entry, values=(["admin", "gerente", "cajero"]), variable=self.selected_profile)
        self.opm_profile.grid(row=2, column=3, pady=5)
        
        frame = Frame(fr_table)
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
        
        self.table['columns'] = ("ID", "Nombre", "Username", "Contraseña", "Perfil")
        self.table.column("#0", width=0, stretch=False)
        self.table.column("ID", anchor="center", width=30)
        self.table.column("Nombre", anchor="center", width=150)
        self.table.column("Username", anchor="center", width=150)
        self.table.column("Contraseña", anchor="center", width=150)
        self.table.column("Perfil", anchor="center", width=150)
        
        self.table.heading("#0", text="", anchor="center")
        self.table.heading("ID", text="ID", anchor="center")
        self.table.heading("Nombre", text="Nombre", anchor="center")
        self.table.heading("Username", text="Username", anchor="center")
        self.table.heading("Contraseña", text="Contraseña", anchor="center")
        self.table.heading("Perfil", text="Perfil", anchor="center")
        
        self.bt_new = Button(fr_button, text="Nuevo", border_width=1, width=60, command=self.new_user)
        self.bt_new.grid(row=0, column=0, padx=5, pady=10)
        self.bt_save = Button(fr_button, text="Salvar", border_width=1, width=60, command=self.save_user)
        self.bt_save.grid(row=0, column=1, padx=5, pady=10)
        self.bt_cancel = Button(fr_button, text="Cancelar", border_width=1, width=60, command=self.default)
        self.bt_cancel.grid(row=0, column=2, padx=5, pady=10)
        self.bt_edit = Button(fr_button, text="Editar", border_width=1, width=60, command=self.edit_user)
        self.bt_edit.grid(row=0, column=3, padx=5, pady=10)
        self.bt_remove = Button(fr_button, text="Eliminar", border_width=1, width=60, command=self.remove_user)
        self.bt_remove.grid(row=0, column=4, padx=5, pady=10)
        self.bt_return = Button(fr_button, text="Regresar", border_width=1, width=60, command=self._return)
        self.bt_return.grid(row=0, column=5, padx=5, pady=10)
        
        self.default()
        self.update_table()
        
    def search_user(self) -> None:
        if not self.tx_search.get().isdecimal():
            messagebox.showwarning("Error", "Ingrese un ID válido")
            return
        
        def search_id():
            for item in self.table.get_children():
                item_values = self.table.item(item, "values")
                
                if item_values[0] == self.tx_search.get():
                    return item
            return None
        
        id = search_id()
        print("id -> ", id)
        if id is None:
            messagebox.showinfo(">_<", "No se encontro el usuario")
            return
        
        self.table.selection_set(id)
        self.table.focus(id)
        self.table.see(id)
    
    def remove_user(self) -> None:
        try:
            selected = self.table.focus()
            if selected is None or selected == "":
                messagebox.showinfo(">_<", "No se selecciono un usuario")
                return
            
            values = self.table.item(selected, "values")
            aux = user_class(id=int(values[0]))
            db_user.remove(self, aux)
            messagebox.showinfo(">u<", "Usuario eliminado")
            self.update_table()
            self.default()
        except Exception as err:
            print("[-] remove_user", err)
            messagebox.showerror("Error", "No se logro eliminar el usuario")
        
    def new_user(self) -> None:
        self.tx_id.configure(state=ENABLE)
        self.tx_name.configure(state=ENABLE)
        self.tx_username.configure(state=ENABLE)
        self.tx_password.configure(state=ENABLE)
        self.opm_profile.configure(state=ENABLE)
        
        self.bt_new.configure(state=DISABLED)
        self.bt_save.configure(state=ENABLE)
        self.bt_cancel.configure(state=ENABLE)
        self.bt_edit.configure(state=DISABLED)
        self.bt_remove.configure(state=DISABLED)
        
        self.clear_user()
        self.tx_id.insert(0, db_user.get_max_id(self)+1)
        self.tx_id.configure(state=DISABLED)
        self.band = True
        return
        
    def save_user(self) -> None:
        try:
            self.validate()
        except Exception as error:
            messagebox.showwarning("Error >_<", error)
            return
        
        if len(self.tx_password.get()) < 6:
            messagebox.showwarning("Contraseña demasiado corta", "La contraseña debe tener al menos 6 caracteres")
            return
        
        try:
            user = user_class(int(self.tx_id.get()),self.tx_name.get(), self.tx_username.get(), self.tx_password.get(), self.opm_profile.get())
            if self.band == True:
                db_user.save(self, user)
                messagebox.showinfo("Exitoso", "Usuario guardado exitosamente!")
            else:
                db_user.edit(self, user)
                messagebox.showinfo("Exitoso", "Usuario editado exitosamente!")
            self.default()
            self.update_table()
        except Exception as err:
            print(f"[-] saveUser: {err}")
            messagebox.showerror("Error", f"Error al {"guardar" if self.band else "editar"} usuario en BD")
        finally:
            self.band = None
    
    def get_user(self) -> None:
        selected = self.table.focus()
        if selected is None or selected == "":
            raise Exception("No se encontro el usuario")
        
        values = self.table.item(selected, "values")
        self.enable_edit()
        self.tx_id.insert(0, values[0])
        self.tx_id.configure(state=DISABLED)
        self.tx_name.insert(0, values[1])
        self.tx_username.insert(0, values[2])
        self.tx_password.insert(0, values[3])
        self.opm_profile.set(values[4])
    
    def edit_user(self) -> None:
        try:
            self.get_user()
        except Exception as err:
            print("[-] ", err)
            messagebox.showinfo("._.", err)
            return
        
        self.band = False
    
    def _return(self) -> None:
        self.controller.show_frame("Menu")
    
    def clear_user(self):
        self.tx_id.delete(0, END)
        self.tx_name.delete(0, END)
        self.tx_username.delete(0, END)
        self.tx_password.delete(0, END)
        self.opm_profile.set("admin")
    
    def default(self):
        self.tx_id.configure(state=ENABLE)
        self.clear_user()
        self.bt_edit.configure(state=ENABLE)
        self.bt_new.configure(state=ENABLE)
        self.bt_save.configure(state=DISABLED)
        self.bt_cancel.configure(state=DISABLED)
        self.bt_remove.configure(state=ENABLE)
        
        self.tx_id.configure(state=DISABLED)
        self.tx_name.configure(state=DISABLED)
        self.tx_username.configure(state=DISABLED)
        self.tx_password.configure(state=DISABLED)
        self.opm_profile.configure(state=DISABLED)
    
    def enable_edit(self):
        self.bt_new.configure(state=DISABLED)
        self.bt_save.configure(state=ENABLE)
        self.bt_cancel.configure(state=ENABLE)
        self.bt_edit.configure(state=DISABLED)
        self.bt_remove.configure(state=DISABLED)
        
        self.tx_id.configure(state=ENABLE)
        self.tx_name.configure(state=ENABLE)
        self.tx_username.configure(state=ENABLE)
        self.tx_password.configure(state=ENABLE)
        self.opm_profile.configure(state=ENABLE)
        self.clear_user()
    
    def insert_table(self, data: list) -> None:
        for i, row in enumerate(data):
            self.table.insert("", "end", iid=i, values=row)
            
    def clear_table(self) -> None:
        self.table.delete(*self.table.get_children())
        
    def update_table(self) -> None:
        self.clear_table()
        users = db_user.get_all_users(self)
        # print(users)
        self.insert_table(users)
    
    
    def validate(self) -> None:
        # Empty
        entry_empty(self.tx_id, "ID")
        entry_empty(self.tx_name, "Nombre")
        entry_empty(self.tx_username, "Username")
        entry_empty(self.tx_password, "Contraseña")
        entry_empty(self.opm_profile, "Perfil")
        
        # Exist
        if self.band == True:
            if not name_available(self.tx_username.get(), "user"):
                raise Exception("Username ya existe")
        
        # Type
        if not self.tx_id.get().isdecimal():
            raise Exception("ID debe ser un número")
        
        if not is_alphabetic(self.tx_name.get()):
            raise Exception("Nombre inválido")
        
        if not self.tx_username.get().isalnum():
            raise Exception("Username debe ser solo letras y números")
        
        if self.opm_profile.get() not in ["admin", "gerente", "cajero"]:
            raise Exception("Perfil debe ser admin, gerente o cajero")
        
        # Size
        if len(self.tx_password.get()) < 6:
            raise Exception("Contraseña debe tener al menos 6 caracteres")

        if len(self.tx_name.get()) > 30:
            raise Exception("Nombre debe tener máximo 30 caracteres")
        
        if len(self.tx_username.get()) > 30:
            raise Exception("Username debe tener máximo 30 caracteres")
        
        if len(self.tx_password.get()) > 30:
            raise Exception("Contraseña debe tener máximo 30 caracteres")