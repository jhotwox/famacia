from customtkinter import END, CTkButton as Button, CTkEntry as Entry, CTkLabel as Label, DISABLED, NORMAL as ENABLE, CTkFrame as Frame, CTkScrollbar as Scrollbar
from tkinter import messagebox
from tkinter.ttk import Treeview
from functions import entry_empty, is_alphabetic, is_numeric
from db_supplier import db_supplier
from supplier import supplier as supplier_class
from table_style import apply_style
from db_functions import name_available

class Suppliers(Frame):
    def __init__(self, container, controller, profile: supplier_class, *args, **kwargs):
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
        self.bt_search = Button(fr_search, text="Buscar", border_width=2, width=100, command=self.search_supplier)
        self.bt_search.grid(row=0, column=2, padx=5, pady=10)

        self.lb_id = Label(fr_entry, text="ID")
        self.lb_id.grid(row=0, column=0, pady=0, sticky="w")
        self.tx_id = Entry(fr_entry, placeholder_text="ID")
        self.tx_id.grid(row=0, column=1, pady=5)

        self.lb_name = Label(fr_entry, text="Nombre")
        self.lb_name.grid(row=1, column=0, pady=0, sticky="w")
        self.tx_name = Entry(fr_entry, placeholder_text="Nombre")
        self.tx_name.grid(row=1, column=1, pady=5, padx=20)
        self.lb_bank_code = Label(fr_entry, text="Clave bancaria")
        self.lb_bank_code.grid(row=1, column=2, pady=0, sticky="w")
        self.tx_bank_code = Entry(fr_entry, placeholder_text="Clave bancaria")
        self.tx_bank_code.grid(row=1, column=3, pady=5, padx=20)

        self.lb_address = Label(fr_entry, text="Dirección")
        self.lb_address.grid(row=2, column=0, pady=0, sticky="w")
        self.tx_address = Entry(fr_entry, placeholder_text="Dirección")
        self.tx_address.grid(row=2, column=1, pady=5, padx=20)
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
        
        self.table['columns'] = ("ID", "Nombre", "Clave bancaria", "Dirección", "Teléfono")
        self.table.column("#0", width=0, stretch=False)
        self.table.column("ID", anchor="center", width=30)
        self.table.column("Nombre", anchor="center", width=150)
        self.table.column("Clave bancaria", anchor="center", width=150)
        self.table.column("Dirección", anchor="center", width=150)
        self.table.column("Teléfono", anchor="center", width=150)
        
        self.table.heading("#0", text="", anchor="center")
        self.table.heading("ID", text="ID", anchor="center")
        self.table.heading("Nombre", text="Nombre", anchor="center")
        self.table.heading("Clave bancaria", text="Clave bancaria", anchor="center")
        self.table.heading("Dirección", text="Dirección", anchor="center")
        self.table.heading("Teléfono", text="Teléfono", anchor="center")
        
        self.bt_new = Button(fr_button, text="Nuevo", border_width=1, width=60, command=self.new_supplier)
        self.bt_new.grid(row=0, column=0, padx=5, pady=10)
        self.bt_save = Button(fr_button, text="Salvar", border_width=1, width=60, command=self.save_supplier)
        self.bt_save.grid(row=0, column=1, padx=5, pady=10)
        self.bt_cancel = Button(fr_button, text="Cancelar", border_width=1, width=60, command=self.default)
        self.bt_cancel.grid(row=0, column=2, padx=5, pady=10)
        self.bt_edit = Button(fr_button, text="Editar", border_width=1, width=60, command=self.edit_supplier)
        self.bt_edit.grid(row=0, column=3, padx=5, pady=10)
        self.bt_remove = Button(fr_button, text="Eliminar", border_width=1, width=60, command=self.remove_supplier)
        self.bt_remove.grid(row=0, column=4, padx=5, pady=10)
        self.bt_return = Button(fr_button, text="Regresar", border_width=1, width=60, command=self._return)
        self.bt_return.grid(row=0, column=5, padx=5, pady=10)
        
        self.default()
        self.update_table()
        
    def search_supplier(self) -> None:
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
            messagebox.showinfo(">_<", "No se encontro el proveedor")
            return
        
        self.table.selection_set(id)
        self.table.focus(id)
        self.table.see(id)
    
    def remove_supplier(self) -> None:
        try:
            selected = self.table.focus()
            if selected is None or selected == "":
                messagebox.showinfo(">_<", "No se selecciono un proveedor")
                return
            
            values = self.table.item(selected, "values")
            aux = supplier_class(id=int(values[0]))
            db_supplier.remove(self, aux)
            messagebox.showinfo(">u<", "Proveedor eliminado")
            self.update_table()
            self.default()
        except Exception as err:
            print("[-] remove_supplier", err)
            messagebox.showerror("Error", "No se logro eliminar el proveedor")
        
    def new_supplier(self) -> None:
        self.tx_id.configure(state=ENABLE)
        self.tx_name.configure(state=ENABLE)
        self.tx_bank_code.configure(state=ENABLE)
        self.tx_address.configure(state=ENABLE)
        self.tx_phone.configure(state=ENABLE)
        
        self.bt_new.configure(state=DISABLED)
        self.bt_save.configure(state=ENABLE)
        self.bt_cancel.configure(state=ENABLE)
        self.bt_edit.configure(state=DISABLED)
        self.bt_remove.configure(state=DISABLED)
        
        self.clear_supplier()
        self.tx_id.insert(0, db_supplier.get_max_id(self)+1)
        self.tx_id.configure(state=DISABLED)
        self.band = True
        return
    
    def validate(self) -> None:
        # Empty
        entry_empty(self.tx_id, "ID")
        entry_empty(self.tx_name, "Nombre")
        entry_empty(self.tx_bank_code, "Clave bancaria")
        entry_empty(self.tx_address, "Dirección")
        entry_empty(self.tx_phone, "Teléfono")
        
        # Exist
        if self.band == True:
            if not name_available(self.tx_name.get(), "supplier"):
                raise Exception("Nombre ya existe")
        
        # Type
        if not self.tx_id.get().isdecimal():
            raise Exception("ID debe ser un número")
        
        if not is_alphabetic(self.tx_name.get()):
            raise Exception("Nombre inválido")
        
        if not is_numeric(self.tx_bank_code.get()):
            raise Exception("Clave bancaria debe ser un número")
        
        if not self.tx_phone.get().isdecimal():
            raise Exception("Teléfono debe ser un número")
        
        # Size
        if len(self.tx_phone.get()) < 10:
            raise Exception("Teléfono debe tener al menos 10 números")

        if len(self.tx_phone.get()) > 13:
            raise Exception("Teléfono debe tener máximo 13 números")

        if len(self.tx_name.get()) > 30:
            raise Exception("Nombre debe tener máximo 30 caracteres")
        
        if len(self.tx_address.get()) > 50:
            raise Exception("Dirección debe tener máximo 50 caracteres")
        
        if len(self.tx_bank_code.get()) > 20:
            raise Exception("Clave bancaria debe tener máximo 20 caracteres")
        
    def save_supplier(self) -> None:
        try:
            self.validate()
        except Exception as error:
            messagebox.showwarning("Error >_<", error)
            return
        
        try:
            supplier = supplier_class(int(self.tx_id.get()), self.tx_phone.get(), self.tx_name.get(), self.tx_address.get(), self.tx_bank_code.get())
            if self.band == True:
                db_supplier.save(self, supplier)
                messagebox.showinfo("Exitoso", "Proveedor guardado exitosamente!")
            else:
                db_supplier.edit(self, supplier)
                messagebox.showinfo("Exitoso", "Proveedor editado exitosamente!")
            self.default()
            self.update_table()
        except Exception as err:
            print(f"[-] saveSupplier: {err}")
            messagebox.showerror("Error", f"Error al {"guardar" if self.band else "editar"} proveedor en BD")
        finally:
            self.band = None
    
    def get_supplier(self) -> None:
        selected = self.table.focus()
        if selected is None or selected == "":
            raise Exception("No se encontro el proveedor")
        
        values = self.table.item(selected, "values")
        self.enable_edit()
        self.tx_id.insert(0, values[0])
        self.tx_id.configure(state=DISABLED)
        self.tx_name.insert(0, values[1])
        self.tx_bank_code.insert(0, values[2])
        self.tx_address.insert(0, values[3])
        self.tx_phone.insert(0, values[4])

    def edit_supplier(self) -> None:
        try:
            self.get_supplier()
        except Exception as err:
            print("[-] ", err)
            messagebox.showinfo("._.", err)
            return
        
        self.band = False
    
    def _return(self) -> None:
        self.controller.show_frame("Menu")
    
    def clear_supplier(self):
        self.tx_id.delete(0, END)
        self.tx_name.delete(0, END)
        self.tx_bank_code.delete(0, END)
        self.tx_address.delete(0, END)
        self.tx_phone.delete(0, END)
    
    def default(self):
        self.tx_id.configure(state=ENABLE)
        self.clear_supplier()
        self.bt_edit.configure(state=ENABLE)
        self.bt_new.configure(state=ENABLE)
        self.bt_save.configure(state=DISABLED)
        self.bt_cancel.configure(state=DISABLED)
        self.bt_remove.configure(state=ENABLE)
        
        self.tx_id.configure(state=DISABLED)
        self.tx_name.configure(state=DISABLED)
        self.tx_bank_code.configure(state=DISABLED)
        self.tx_address.configure(state=DISABLED)
        self.tx_phone.configure(state=DISABLED)
    
    def enable_edit(self):
        self.bt_new.configure(state=DISABLED)
        self.bt_save.configure(state=ENABLE)
        self.bt_cancel.configure(state=ENABLE)
        self.bt_edit.configure(state=DISABLED)
        self.bt_remove.configure(state=DISABLED)
        
        self.tx_id.configure(state=ENABLE)
        self.tx_name.configure(state=ENABLE)
        self.tx_bank_code.configure(state=ENABLE)
        self.tx_address.configure(state=ENABLE)
        self.tx_phone.configure(state=ENABLE)
        self.clear_supplier()
    
    def insert_table(self, data: list) -> None:
        for i, row in enumerate(data):
            self.table.insert("", "end", iid=i, values=row)
            
    def clear_table(self) -> None:
        self.table.delete(*self.table.get_children())
        
    def update_table(self) -> None:
        self.clear_table()
        suppliers = db_supplier.get_all_suppliers(self)
        # print(suppliers)
        self.insert_table(suppliers)