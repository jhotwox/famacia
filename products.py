from customtkinter import END, CTkButton as Button, CTkEntry as Entry, CTkLabel as Label, CTk, DISABLED, NORMAL as ENABLE, CTkFrame as Frame, CTkOptionMenu as OptMenu, StringVar, CTkScrollbar as Scrollbar
from tkinter import messagebox
from tkinter.ttk import Treeview
from functions import entry_empty, find_id, is_alphabetic, is_numeric
from db_product import db_product
from product import product as product_class
from table_style import apply_style
from db_supplier import db_supplier
from db_functions import name_available

class Products(Frame):
    def __init__(self, container, controller, profile: product_class, *args, **kwargs):
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
        self.bt_search = Button(fr_search, text="Buscar", border_width=2, width=100, command=self.search_product)
        self.bt_search.grid(row=0, column=2, padx=5, pady=10)

        self.lb_id = Label(fr_entry, text="ID")
        self.lb_id.grid(row=0, column=0, pady=0, sticky="w")
        self.tx_id = Entry(fr_entry, placeholder_text="ID")
        self.tx_id.grid(row=0, column=1, pady=5)

        self.lb_name = Label(fr_entry, text="Nombre")
        self.lb_name.grid(row=1, column=0, pady=0, sticky="w")
        self.tx_name = Entry(fr_entry, placeholder_text="Nombre")
        self.tx_name.grid(row=1, column=1, pady=5, padx=20)
        self.lb_description = Label(fr_entry, text="Descripción")
        self.lb_description.grid(row=1, column=2, pady=0, sticky="w")
        self.tx_description = Entry(fr_entry, placeholder_text="Descripción")
        self.tx_description.grid(row=1, column=3, pady=5, padx=20)

        self.lb_stock = Label(fr_entry, text="Stock")
        self.lb_stock.grid(row=2, column=0, pady=0, sticky="w")
        self.tx_stock = Entry(fr_entry, placeholder_text="Stock")
        self.tx_stock.grid(row=2, column=1, pady=5, padx=20)
        self.lb_discount = Label(fr_entry, text="Descuento")
        self.lb_discount.grid(row=2, column=2, pady=0, sticky="w")
        self.tx_discount = Entry(fr_entry, placeholder_text="0 - 100")
        self.tx_discount.grid(row=2, column=3, pady=5, padx=20)

        self.lb_sale_price = Label(fr_entry, text="Precio venta")
        self.lb_sale_price.grid(row=3, column=0, pady=0, sticky="w")
        self.tx_sale_price = Entry(fr_entry, placeholder_text="Precio venta")
        self.tx_sale_price.grid(row=3, column=1, pady=5, padx=20)
        self.lb_purchase_price = Label(fr_entry, text="Precio compra")
        self.lb_purchase_price.grid(row=3, column=2, pady=0, sticky="w")
        self.tx_purchase_price = Entry(fr_entry, placeholder_text="Precio compra")
        self.tx_purchase_price.grid(row=3, column=3, pady=5, padx=20)
        
        self.lb_category = Label(fr_entry, text="Categoria")
        self.lb_category.grid(row=4, column=0, pady=0, sticky="w")
        self.tx_category = Entry(fr_entry, placeholder_text="Categoria")
        self.tx_category.grid(row=4, column=1, pady=5, padx=20)
        self.suppliers = db_supplier.get_suppliers(self)
        # print(self.suppliers)
        self.lb_supplier = Label(fr_entry, text="Proveedor")
        self.lb_supplier.grid(row=4, column=2, pady=0, sticky="w")
        self.selected_supplier = StringVar(value=next(iter(self.suppliers.values())) if len(self.suppliers) > 0 else "No disponible")
        self.opm_supplier = OptMenu(fr_entry, values=list(self.suppliers.values()), variable=self.selected_supplier)
        self.opm_supplier.grid(row=4, column=3, pady=5, padx=20)
        
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
        
        self.table['columns'] = ("ID", "Nombre", "Descripción", "Venta", "Compra", "Descuento", "Stock", "Categoría", "Proveedor")
        self.table.column("#0", width=0, stretch=False)
        self.table.column("ID", anchor="center", width=30)
        self.table.column("Nombre", anchor="center", width=150)
        self.table.column("Descripción", anchor="center", width=150)
        self.table.column("Venta", anchor="center", width=50)
        self.table.column("Compra", anchor="center", width=70)
        self.table.column("Descuento", anchor="center", width=70)
        self.table.column("Stock", anchor="center", width=50)
        self.table.column("Categoría", anchor="center", width=150)
        self.table.column("Proveedor", anchor="center", width=50)
        
        self.table.heading("#0", text="", anchor="center")
        self.table.heading("ID", text="ID", anchor="center")
        self.table.heading("Nombre", text="Nombre", anchor="center")
        self.table.heading("Descripción", text="Descripción", anchor="center")
        self.table.heading("Venta", text="Venta", anchor="center")
        self.table.heading("Compra", text="Compra", anchor="center")
        self.table.heading("Descuento", text="Descuento", anchor="center")
        self.table.heading("Stock", text="Stock", anchor="center")
        self.table.heading("Categoría", text="Categoría", anchor="center")
        self.table.heading("Proveedor", text="Proveedor", anchor="center")
        
        self.bt_new = Button(fr_button, text="Nuevo", border_width=1, width=60, command=self.new_product)
        self.bt_new.grid(row=0, column=0, padx=5, pady=10)
        self.bt_save = Button(fr_button, text="Salvar", border_width=1, width=60, command=self.save_product)
        self.bt_save.grid(row=0, column=1, padx=5, pady=10)
        self.bt_cancel = Button(fr_button, text="Cancelar", border_width=1, width=60, command=self.default)
        self.bt_cancel.grid(row=0, column=2, padx=5, pady=10)
        self.bt_edit = Button(fr_button, text="Editar", border_width=1, width=60, command=self.edit_product)
        self.bt_edit.grid(row=0, column=3, padx=5, pady=10)
        self.bt_remove = Button(fr_button, text="Eliminar", border_width=1, width=60, command=self.remove_product)
        self.bt_remove.grid(row=0, column=4, padx=5, pady=10)
        self.bt_update = Button(fr_button, text="Actualizar", border_width=1, width=60, command=self.update_table)
        self.bt_update.grid(row=0, column=5, padx=5, pady=10)
        self.bt_return = Button(fr_button, text="Regresar", border_width=1, width=60, command=self._return)
        self.bt_return.grid(row=0, column=6, padx=5, pady=10)
        
        self.default()
        self.update_table()
        
    def search_product(self) -> None:
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
        # print("id -> ", id)
        if id is None:
            messagebox.showinfo(">_<", "No se encontro el producto")
            return
        
        self.table.selection_set(id)
        self.table.focus(id)
        self.table.see(id)
    
    def remove_product(self) -> None:
        try:
            selected = self.table.focus()
            if selected is None or selected == "":
                messagebox.showinfo(">_<", "No se selecciono un producto")
                return
            
            values = self.table.item(selected, "values")
            aux = product_class(id=int(values[0]))
            db_product.remove(self, aux)
            messagebox.showinfo(">u<", "Producto eliminado")
            self.update_table()
            self.default()
        except Exception as err:
            print("[-] remove_product", err)
            messagebox.showerror("Error", "No se logro eliminar el producto")
    
    def new_product(self) -> None:
        self.tx_id.configure(state=ENABLE)
        self.tx_name.configure(state=ENABLE)
        self.tx_description.configure(state=ENABLE)
        self.tx_stock.configure(state=ENABLE)
        self.tx_discount.configure(state=ENABLE)
        self.tx_sale_price.configure(state=ENABLE)
        self.tx_purchase_price.configure(state=ENABLE)
        self.tx_category.configure(state=ENABLE)
        self.opm_supplier.configure(state=ENABLE)
        
        self.bt_new.configure(state=DISABLED)
        self.bt_save.configure(state=ENABLE)
        self.bt_cancel.configure(state=ENABLE)
        self.bt_edit.configure(state=DISABLED)
        self.bt_remove.configure(state=DISABLED)
        
        self.clear_product()
        self.tx_id.insert(0, db_product.get_max_id(self)+1)
        self.tx_id.configure(state=DISABLED)
        self.band = True
        return
    
    def save_product(self) -> None:
        try:
            self.validate()
        except Exception as error:
            messagebox.showwarning("Error >_<", error)
            return
        
        try:
            supplier = find_id(self.suppliers, self.opm_supplier.get())
            # print("Supplier ID -> ", supplier)
            user = product_class(int(self.tx_id.get()), self.tx_name.get(), self.tx_description.get(), float(self.tx_sale_price.get()), float(self.tx_purchase_price.get()), int(self.tx_discount.get()), int(self.tx_stock.get()), self.tx_category.get(), supplier)
            if self.band == True:
                db_product.save(self, user)
                messagebox.showinfo("Exitoso", "Producto guardado exitosamente!")
            else:
                db_product.edit(self, user)
                messagebox.showinfo("Exitoso", "Producto editado exitosamente!")
            self.default()
            self.update_table()
        except Exception as err:
            print(f"[-] saveUser: {err}")
            messagebox.showerror("Error", f"Error al {"guardar" if self.band else "editar"} producto en BD")
        finally:
            self.band = None
    
    def get_product(self) -> None:
        selected = self.table.focus()
        if selected is None or selected == "":
            raise Exception("No se encontro el producto")
        
        values = self.table.item(selected, "values")
        self.enable_edit()
        self.tx_id.insert(0, values[0])
        self.tx_id.configure(state=DISABLED)
        self.tx_name.insert(0, values[1])
        self.tx_description.insert(0, values[2])
        self.tx_sale_price.insert(0, values[3])
        self.tx_purchase_price.insert(0, values[4])
        self.tx_discount.insert(0, values[5])
        self.tx_stock.insert(0, values[6])
        self.tx_category.insert(0, values[7])
        try:
            self.opm_supplier.set(self.suppliers[int(values[8])])
        except Exception as err:
            raise err
    
    def edit_product(self) -> None:
        try:
            self.get_product()
        except Exception as err:
            print("[-] ", err)
            messagebox.showinfo("._.", err)
            return
        
        self.band = False
    
    def _return(self) -> None:
        self.controller.show_frame("Menu")
    
    def clear_product(self):
        self.tx_id.delete(0, END)
        self.tx_name.delete(0, END)
        self.tx_description.delete(0, END)
        self.tx_sale_price.delete(0, END)
        self.tx_purchase_price.delete(0, END)
        self.tx_discount.delete(0, END)
        self.tx_stock.delete(0, END)
        self.tx_category.delete(0, END)
        self.opm_supplier.configure(values=list(self.suppliers.values()))
        self.opm_supplier.set(next(iter(self.suppliers.values())) if len(self.suppliers) > 0 else "No disponible")
    
    def default(self):
        self.tx_id.configure(state=ENABLE)
        self.clear_product()
        self.bt_edit.configure(state=ENABLE)
        self.bt_new.configure(state=ENABLE)
        self.bt_save.configure(state=DISABLED)
        self.bt_cancel.configure(state=DISABLED)
        self.bt_remove.configure(state=ENABLE)
        
        self.tx_id.configure(state=DISABLED)
        self.tx_name.configure(state=DISABLED)
        self.tx_description.configure(state=DISABLED)
        self.tx_sale_price.configure(state=DISABLED)
        self.tx_purchase_price.configure(state=DISABLED)
        self.tx_discount.configure(state=DISABLED)
        self.tx_stock.configure(state=DISABLED)
        self.tx_category.configure(state=DISABLED)
        self.opm_supplier.configure(state=DISABLED)
    
    def enable_edit(self):
        self.bt_new.configure(state=DISABLED)
        self.bt_save.configure(state=ENABLE)
        self.bt_cancel.configure(state=ENABLE)
        self.bt_edit.configure(state=DISABLED)
        self.bt_remove.configure(state=DISABLED)
        
        self.tx_id.configure(state=ENABLE)
        self.tx_name.configure(state=ENABLE)
        self.tx_description.configure(state=ENABLE)
        self.tx_sale_price.configure(state=ENABLE)
        self.tx_purchase_price.configure(state=ENABLE)
        self.tx_discount.configure(state=ENABLE)
        self.tx_stock.configure(state=ENABLE)
        self.tx_category.configure(state=ENABLE)
        self.opm_supplier.configure(state=ENABLE)
        self.clear_product()
    
    def insert_table(self, data: list) -> None:
        for i, row in enumerate(data):
            self.table.insert("", "end", iid=i, values=row)
            
    def clear_table(self) -> None:
        self.table.delete(*self.table.get_children())
        
    def update_table(self) -> None:
        self.clear_table()
        products = db_product.get_all_products(self)
        self.insert_table(products)

    def validate(self) -> None:
        # Empty
        entry_empty(self.tx_id, "ID")
        entry_empty(self.tx_category, "Categoría")
        entry_empty(self.tx_name, "Nombre")
        entry_empty(self.tx_description, "Descripción")
        entry_empty(self.tx_sale_price, "Venta")
        entry_empty(self.tx_purchase_price, "Compra")
        entry_empty(self.tx_discount, "Descuento")
        entry_empty(self.tx_stock, "Stock")
        
        if self.selected_supplier == "":
            raise Exception("Seleccione un proveedor")
        
        # Exist
        if self.band == True:
            if not name_available(self.tx_name.get(), "product"):
                raise Exception("Nombre ya existe")
        
        if self.selected_supplier == "No disponible":
            raise Exception("No hay proveedores disponibles")
        
        # Type
        if not self.tx_id.get().isdecimal():
            raise Exception("ID debe ser un número")
        
        if not is_alphabetic(self.tx_name.get()):
            raise Exception("Nombre inválido")
        
        if not is_numeric(self.tx_sale_price.get()):
            raise Exception("Precio de venta debe ser un número")
        
        if not is_numeric(self.tx_purchase_price.get()):
            raise Exception("Precio de compra debe ser un número")
        
        if not self.tx_discount.get().isdecimal():
            raise Exception("Descuento debe ser un número decimal")
        
        if not self.tx_stock.get().isdecimal():
            raise Exception("Stock debe ser un número decimal")
        
        if not is_alphabetic(self.tx_category.get()):
            raise Exception("Categoria invalida")
        
        if self.opm_supplier.get() not in list(self.suppliers.values()):
            raise Exception("El proveedor no esta listado")
        
        # Size
        if len(self.tx_name.get()) > 30:
            raise Exception("Nombre debe tener máximo 30 caracteres")
        
        if len(self.tx_description.get()) > 30:
            raise Exception("Descripción debe tener máximo 30 caracteres")
        
        if len(self.tx_category.get()) > 30:
            raise Exception("Categoria debe tener máximo 30 caracteres")
        
        try:
            if not (0 <= int(self.tx_discount.get()) <= 100):
                raise Exception("Descuento debe ser un número entre 0 y 100")
        except :
            raise Exception("Descuento debe ser un número decimal")
