from customtkinter import END, CTkButton as Button, CTkEntry as Entry, CTkLabel as Label, DISABLED, NORMAL as ENABLE, CTkFrame as Frame, CTkScrollbar as Scrollbar
from tkinter import messagebox
from tkinter.ttk import Treeview
from functions import entry_empty, is_alphabetic, is_numeric
from db_customer import db_customer
from customer import customer as customer_class
from table_style import apply_style
from db_functions import name_available

class Customers(Frame):
    def __init__(self, container, controller, profile: customer_class, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        
        self.controller = controller
        self.band = None
        self.profile = profile
        
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
        self.bt_search = Button(fr_search, text="Buscar", border_width=2, width=100, command=self.search_customer)
        self.bt_search.grid(row=0, column=2, padx=5, pady=10)

        self.lb_id = Label(fr_entry, text="ID")
        self.lb_id.grid(row=0, column=0, pady=0, sticky="w")
        self.tx_id = Entry(fr_entry, placeholder_text="ID")
        self.tx_id.grid(row=0, column=1, pady=5)

        self.lb_name = Label(fr_entry, text="Nombre")
        self.lb_name.grid(row=1, column=0, pady=0, sticky="w")
        self.tx_name = Entry(fr_entry, placeholder_text="Nombre")
        self.tx_name.grid(row=1, column=1, pady=5, padx=20)
        self.lb_points = Label(fr_entry, text="Puntos")
        self.lb_points.grid(row=1, column=2, pady=0, sticky="w")
        self.tx_points = Entry(fr_entry, placeholder_text="Puntos")
        self.tx_points.grid(row=1, column=3, pady=5, padx=20)

        self.lb_adress = Label(fr_entry, text="Dirección")
        self.lb_adress.grid(row=2, column=0, pady=0, sticky="w")
        self.tx_adress = Entry(fr_entry, placeholder_text="Dirección")
        self.tx_adress.grid(row=2, column=1, pady=5, padx=20)
        self.lb_phone = Label(fr_entry, text="Teléfono")
        self.lb_phone.grid(row=2, column=2, pady=0, sticky="w")
        self.tx_phone = Entry(fr_entry, placeholder_text="Teléfono")
        self.tx_phone.grid(row=2, column=3, pady=5, padx=20)
        
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
        
        self.table['columns'] = ("ID", "Nombre", "Puntos", "Dirección", "Teléfono")
        self.table.column("#0", width=0, stretch=False)
        self.table.column("ID", anchor="center", width=30)
        self.table.column("Nombre", anchor="center", width=150)
        self.table.column("Puntos", anchor="center", width=150)
        self.table.column("Dirección", anchor="center", width=150)
        self.table.column("Teléfono", anchor="center", width=150)
        
        self.table.heading("#0", text="", anchor="center")
        self.table.heading("ID", text="ID", anchor="center")
        self.table.heading("Nombre", text="Nombre", anchor="center")
        self.table.heading("Puntos", text="Puntos", anchor="center")
        self.table.heading("Dirección", text="Dirección", anchor="center")
        self.table.heading("Teléfono", text="Teléfono", anchor="center")
        
        self.bt_new = Button(fr_button, text="Nuevo", border_width=1, width=60, command=self.new_customer)
        self.bt_new.grid(row=0, column=0, padx=5, pady=10)
        self.bt_save = Button(fr_button, text="Salvar", border_width=1, width=60, command=self.save_customer)
        self.bt_save.grid(row=0, column=1, padx=5, pady=10)
        self.bt_cancel = Button(fr_button, text="Cancelar", border_width=1, width=60, command=self.default)
        self.bt_cancel.grid(row=0, column=2, padx=5, pady=10)
        self.bt_edit = Button(fr_button, text="Editar", border_width=1, width=60, command=self.edit_customer)
        self.bt_edit.grid(row=0, column=3, padx=5, pady=10)
        self.bt_remove = Button(fr_button, text="Eliminar", border_width=1, width=60, command=self.remove_customer)
        self.bt_remove.grid(row=0, column=4, padx=5, pady=10)
        self.bt_return = Button(fr_button, text="Regresar", border_width=1, width=60, command=self._return)
        self.bt_return.grid(row=0, column=5, padx=5, pady=10)
        
        self.default()
        self.update_table()
        
    def search_customer(self) -> None:
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
            messagebox.showinfo(">_<", "No se encontro el cliente")
            return
        
        self.table.selection_set(id)
        self.table.focus(id)
        self.table.see(id)
    
    def remove_customer(self) -> None:
        try:
            selected = self.table.focus()
            if selected is None or selected == "":
                messagebox.showinfo(">_<", "No se selecciono un cliente")
                return
            
            values = self.table.item(selected, "values")
            aux = customer_class(id=int(values[0]))
            db_customer.remove(self, aux)
            messagebox.showinfo(">u<", "Cliente eliminado")
            self.update_table()
            self.default()
        except Exception as err:
            print("[-] remove_customer", err)
            messagebox.showerror("Error", "No se logro eliminar el cliente")
        
    def new_customer(self) -> None:
        self.tx_id.configure(state=ENABLE)
        self.tx_name.configure(state=ENABLE)
        self.tx_points.configure(state=ENABLE)
        self.tx_points.insert(0, 0)
        self.tx_points.configure(state=DISABLED)
        self.tx_adress.configure(state=ENABLE)
        self.tx_phone.configure(state=ENABLE)
        
        self.bt_new.configure(state=DISABLED)
        self.bt_save.configure(state=ENABLE)
        self.bt_cancel.configure(state=ENABLE)
        self.bt_edit.configure(state=DISABLED)
        self.bt_remove.configure(state=DISABLED)
        
        self.clear_customer()
        self.tx_id.insert(0, db_customer.get_max_id(self)+1)
        self.tx_id.configure(state=DISABLED)
        self.band = True
        return
            
    def save_customer(self) -> None:
        try:
            self.validate()
        except Exception as error:
            messagebox.showwarning("Error >_<", error)
            return
        
        try:
            user = customer_class(int(self.tx_id.get()), int(self.tx_points.get()), self.tx_name.get(), self.tx_phone.get(), self.tx_adress.get())
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("ID -> ", user.get_id())
            print("Puntos -> ", user.get_points())
            print("nombre -> ", user.get_name())
            print("direccion -> ", user.get_adress())
            print("Telefono -> ", user.get_phone())
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            if self.band == True:
                db_customer.save(self, user)
                messagebox.showinfo("Exitoso", "Cliente guardado exitosamente!")
            else:
                db_customer.edit(self, user)
                messagebox.showinfo("Exitoso", "Cliente editado exitosamente!")
            self.default()
            self.update_table()
        except Exception as err:
            print(f"[-] saveUser: {err}")
            messagebox.showerror("Error", f"Error al {"guardar" if self.band else "editar"} cliente en BD")
        finally:
            self.band = None
    
    def get_customer(self) -> None:
        selected = self.table.focus()
        if selected is None or selected == "":
            raise Exception("No se encontro el cliente")
        
        values = self.table.item(selected, "values")
        self.enable_edit()
        self.tx_id.insert(0, values[0])
        self.tx_id.configure(state=DISABLED)
        self.tx_name.insert(0, values[1])
        self.tx_points.insert(0, values[2])
        self.tx_adress.insert(0, values[3])
        self.tx_phone.insert(0, values[4])
        
    def edit_customer(self) -> None:
        try:
            self.get_customer()
        except Exception as err:
            print("[-] ", err)
            messagebox.showinfo("._.", err)
            return
        
        self.band = False
    
    def _return(self) -> None:
        self.controller.show_frame("Menu")
    
    def clear_customer(self):
        self.tx_id.delete(0, END)
        self.tx_name.delete(0, END)
        self.tx_points.delete(0, END)
        self.tx_adress.delete(0, END)
        self.tx_phone.delete(0, END)
    
    def default(self):
        self.tx_id.configure(state=ENABLE)
        self.tx_points.configure(state=ENABLE)
        self.clear_customer()
        self.bt_edit.configure(state=ENABLE)
        self.bt_new.configure(state=ENABLE)
        self.bt_save.configure(state=DISABLED)
        self.bt_cancel.configure(state=DISABLED)
        self.bt_remove.configure(state=ENABLE)
        
        self.tx_id.configure(state=DISABLED)
        self.tx_name.configure(state=DISABLED)
        self.tx_points.configure(state=DISABLED)
        self.tx_adress.configure(state=DISABLED)
        self.tx_phone.configure(state=DISABLED)
    
    def enable_edit(self):
        self.bt_new.configure(state=DISABLED)
        self.bt_save.configure(state=ENABLE)
        self.bt_cancel.configure(state=ENABLE)
        self.bt_edit.configure(state=DISABLED)
        self.bt_remove.configure(state=DISABLED)
        
        self.tx_id.configure(state=ENABLE)
        self.tx_name.configure(state=ENABLE)
        self.tx_points.configure(state=ENABLE)
        self.tx_adress.configure(state=ENABLE)
        self.tx_phone.configure(state=ENABLE)
        self.clear_customer()
    
    def insert_table(self, data: list) -> None:
        for i, row in enumerate(data):
            self.table.insert("", "end", iid=i, values=row)
            
    def clear_table(self) -> None:
        self.table.delete(*self.table.get_children())
        
    def update_table(self) -> None:
        self.clear_table()
        customers = db_customer.get_all_customers(self)
        # print(customers)
        self.insert_table(customers)
        
    def validate(self) -> None:
        # Empty
        entry_empty(self.tx_id, "ID")
        entry_empty(self.tx_name, "Nombre")
        entry_empty(self.tx_points, "Puntos")
        entry_empty(self.tx_adress, "Dirección")
        entry_empty(self.tx_phone, "Teléfono")
        
        # Exist
        if self.band == True:
            if not name_available(self.tx_name.get(), "customer"):
                raise Exception("Nombre ya existe")
        
        # Type
        if not self.tx_id.get().isdecimal():
            raise Exception("ID debe ser un número")
        
        if not is_alphabetic(self.tx_name.get()):
            raise Exception("Nombre inválido")
        
        if not is_numeric(self.tx_points.get()):
            raise Exception("Puntos debe ser un número")
        
        if not self.tx_phone.get().isdecimal():
            raise Exception("Teléfono debe ser un número")
        
        # Size
        if len(self.tx_phone.get()) < 10:
            raise Exception("Teléfono debe tener al menos 10 números")

        if len(self.tx_phone.get()) > 13:
            raise Exception("Teléfono debe tener máximo 13 números")

        if len(self.tx_name.get()) > 30:
            raise Exception("Nombre debe tener máximo 30 caracteres")
        
        if len(self.tx_adress.get()) > 50:
            raise Exception("Dirección debe tener máximo 50 caracteres")
    