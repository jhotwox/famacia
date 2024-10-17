from customtkinter import END, CTkButton as Button, CTkEntry as Entry, CTkLabel as Label, DISABLED, NORMAL as ENABLE, CTkFrame as Frame, CTkOptionMenu as OptMenu, StringVar, CTkScrollbar as Scrollbar
from tkinter import messagebox
from tkinter.ttk import Treeview
from functions import entry_empty, find_id, is_alphabetic, is_numeric, get_column_from_list, get_datetime
from table_style import apply_style
from db_functions import name_available
from purchase import purchase as purchase_class
from detail_purchase import detail_purchase as detail_purchase_class
from db_purchase import db_purchase
from db_detail_purchase import db_detail_purchase
from datetime import datetime

from db_product import db_product
from product import product as product_class
from db_supplier import db_supplier

class Purchases(Frame):
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
        
        # Search purchase
        lb_search_purchase = Label(fr_search, text="ID compra", font=("Calisto MT", 12))
        lb_search_purchase.grid(row=0, column=0, padx=5)
        self.id_purchases = db_purchase.get_id_purchases(self, self.profile)
        # print("ID Purchases -> ", self.id_purchases)
        self.selected_search_purchase = StringVar(value=self.id_purchases[0] if len(self.id_purchases) > 0 else "No disponible")
        self.selected_search_purchase.trace("w", self.on_selection_search_purchase)
        self.opm_search_purchase = OptMenu(fr_search, values=self.id_purchases, variable=self.selected_search_purchase)
        self.opm_search_purchase.grid(row=0, column=1, padx=10, pady=10)
        # Search product
        lb_search_product = Label(fr_search, text="Producto", font=("Calisto MT", 12))
        lb_search_product.grid(row=0, column=2, padx=5)
        self.search_products = db_product.get_dict_products_by_supplier(self, self.opm_search_purchase.get())
        self.selected_search_product = StringVar(value=next(iter(self.search_products.values())) if len(self.search_products) > 0 else "No disponible")
        self.opm_search_product = OptMenu(fr_search, values=list(self.search_products.values()), variable=self.selected_search_product)
        self.opm_search_product.grid(row=0, column=3, padx=10, pady=10)
        
        self.bt_search = Button(fr_search, text="Buscar", border_width=2, width=100, command=self.search_purchase)
        self.bt_search.grid(row=0, column=4, padx=5, pady=10)

        lb_id = Label(fr_entry, text="ID")
        lb_id.grid(row=0, column=0, pady=0, sticky="w")
        
        self.purchases = self.id_purchases.copy()
        self.selected_purchase = StringVar(value=self.purchases[0] if len(self.purchases) > 0 else "No disponible")
        self.opm_id = OptMenu(fr_entry, values=self.purchases, variable=self.selected_purchase)
        self.opm_id.grid(row=0, column=1, pady=5)
        lb_user_id = Label(fr_entry, text="ID usuario")
        lb_user_id.grid(row=0, column=2, pady=0, sticky="w")
        self.tx_user_id = Entry(fr_entry, placeholder_text="ID usuario")
        self.tx_user_id.insert(0, self.profile.get_id())
        self.tx_user_id.configure(state=DISABLED)
        self.tx_user_id.grid(row=0, column=3, pady=5)

        self.suppliers = db_supplier.get_suppliers(self)
        lb_supplier = Label(fr_entry, text="Proveedor")
        lb_supplier.grid(row=1, column=0, pady=0, sticky="w")
        self.selected_supplier = StringVar(value=next(iter(self.suppliers.values())) if len(self.suppliers) > 0 else "No disponible")
        self.opm_supplier = OptMenu(fr_entry, values=list(self.suppliers.values()), variable=self.selected_supplier)
        self.opm_supplier.grid(row=1, column=1, pady=5, padx=20)
        lb_quantity = Label(fr_entry, text="Cantidad")
        lb_quantity.grid(row=1, column=2, pady=0, sticky="w")
        self.tx_quantity = Entry(fr_entry, placeholder_text="Cantidad")
        self.tx_quantity.grid(row=1, column=3, pady=5, padx=20)

        self.products = db_product.get_dict_products_by_supplier(self, find_id(self.suppliers, self.opm_supplier.get()))
        lb_product = Label(fr_entry, text="Producto")
        lb_product.grid(row=2, column=0, pady=0, sticky="w")
        self.selected_product = StringVar(value=next(iter(self.products.values())) if len(self.products) > 0 else "No disponible")
        self.opm_product = OptMenu(fr_entry, values=list(self.products.values()), variable=self.selected_product)
        self.opm_product.grid(row=2, column=1, pady=5, padx=20)
        lb_unitary_price = Label(fr_entry, text="Precio unitario")
        lb_unitary_price.grid(row=2, column=2, pady=0, sticky="w")
        self.tx_unitary_price = Entry(fr_entry, placeholder_text="Precio unitario")
        self.tx_unitary_price.grid(row=2, column=3, pady=5, padx=20)

        lb_date = Label(fr_entry, text="Fecha")
        lb_date.grid(row=3, column=0, pady=0, sticky="w")
        self.tx_date = Entry(fr_entry, placeholder_text="Fecha")
        self.tx_date.grid(row=3, column=1, pady=5, padx=20)

        
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
        
        self.table['columns'] = ("ID", "Nombre", "Proveedor", "Fecha", "Precio u.", "Cantidad", "Total")
        self.table.column("#0", width=0, stretch=False)
        self.table.column("ID", anchor="center", width=30)
        self.table.column("Nombre", anchor="center", width=150)
        self.table.column("Proveedor", anchor="center", width=90)
        self.table.column("Fecha", anchor="center", width=90)
        self.table.column("Precio u.", anchor="center", width=80)
        self.table.column("Cantidad", anchor="center", width=70)
        self.table.column("Total", anchor="center", width=80)
        
        self.table.heading("#0", text="", anchor="center")
        self.table.heading("ID", text="ID", anchor="center")
        self.table.heading("Nombre", text="Nombre", anchor="center")
        self.table.heading("Proveedor", text="Proveedor", anchor="center")
        self.table.heading("Fecha", text="Fecha", anchor="center")
        self.table.heading("Precio u.", text="Precio u.", anchor="center")
        self.table.heading("Cantidad", text="Cantidad", anchor="center")
        self.table.heading("Total", text="Total", anchor="center")
        
        self.bt_add = Button(fr_button, text="Añadir producto", border_width=1, width=60, command=self.add_purchase)
        self.bt_add.grid(row=0, column=0, padx=5, pady=10)
        self.bt_new = Button(fr_button, text="Nueva compra", border_width=1, width=60, command=self.new_purchase)
        self.bt_new.grid(row=0, column=1, padx=5, pady=10)
        self.bt_save = Button(fr_button, text="Salvar", border_width=1, width=60, command=self.save_purchase)
        self.bt_save.grid(row=0, column=2, padx=5, pady=10)
        self.bt_cancel = Button(fr_button, text="Cancelar", border_width=1, width=60, command=self.default)
        self.bt_cancel.grid(row=0, column=3, padx=5, pady=10)
        self.bt_edit = Button(fr_button, text="Editar", border_width=1, width=60, command=self.edit_purchase)
        self.bt_edit.grid(row=0, column=4, padx=5, pady=10)
        self.bt_remove = Button(fr_button, text="Eliminar", border_width=1, width=60, command=self.remove_product)
        self.bt_remove.grid(row=0, column=5, padx=5, pady=10)
        self.bt_return = Button(fr_button, text="Regresar", border_width=1, width=60, command=self._return)
        self.bt_return.grid(row=0, column=6, padx=5, pady=10)
        
        self.default()
        self.update_table()
    
    def on_selection_search_purchase(self):
        self.search_products = db_product.get_supplier_products(self, self.opm_search_purchase.get())
    
    def search_purchase(self) -> None:
        def search_id():
            for item in self.table.get_children():
                item_values = self.table.item(item, "values")
                if item_values[0] == self.opm_search_purchase.get() and item_values[1] == self.opm_search_product.get():
                    return item
            return None
        
        id = search_id()
        print("id -> ", id)
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
            
            detail_purchase = detail_purchase_class(int(values[0]), find_id(self.products, values[1]))
            db_detail_purchase.remove(self, detail_purchase)
            
            purchase = purchase_class(int(values[0]))
            if db_purchase.count_detail_purchase(self, purchase) == 0:
                db_purchase.remove(self, purchase)
            
            messagebox.showinfo(">u<", "Producto eliminado")
            self.update_table()
            self.default()
        except Exception as err:
            print("[-] remove_product", err)
            messagebox.showerror("Error", "No se logro eliminar el producto")
    
    def add_purchase(self) -> None:
        return
    
    def new_purchase(self) -> None:
        self.opm_id.configure(state=ENABLE)
        self.opm_supplier.configure(state=ENABLE)
        self.tx_quantity.configure(state=ENABLE)
        self.opm_product.configure(state=ENABLE)
        self.tx_unitary_price.configure(state=ENABLE)
        self.tx_date.insert(0, get_datetime())
        self.tx_date.configure(state=DISABLED)
        
        self.bt_add.configure(state=DISABLED)
        self.bt_new.configure(state=DISABLED)
        self.bt_save.configure(state=ENABLE)
        self.bt_cancel.configure(state=ENABLE)
        self.bt_edit.configure(state=DISABLED)
        self.bt_remove.configure(state=DISABLED)
        
        self.clear_purchase()
        self.opm_id.set(db_purchase.get_max_id(self)+1)
        self.opm_id.configure(state=DISABLED)
        self.band = True
    
    def save_purchase(self) -> None:
        try:
            self.validate()
        except Exception as error:
            messagebox.showwarning("Error >_<", error)
            return
        
        try:
            product_id = find_id(self.products, self.opm_product.get())
            # print("Supplier ID -> ", supplier)
            
            detail_purchase = detail_purchase_class(int(self.opm_id.get()), product_id, int(self.tx_quantity.get()), float(self.tx_unitary_price.get()))
            
            if self.band == True:
                total: float = int(self.tx_quantity.get()) * float(self.tx_unitary_price.get())
                purchase = purchase_class(int(self.opm_id.get()), self.tx_date.get(), total, self.profile.get_id())
                db_purchase.save(self, purchase)
                
                db_detail_purchase.save(self, detail_purchase)
                messagebox.showinfo("Exitoso", "Producto guardado exitosamente!")
            elif self.band == False:
                db_detail_purchase.edit(self, detail_purchase)
                messagebox.showinfo("Exitoso", "Producto editado exitosamente!")
            else:
                db_detail_purchase.save(self, detail_purchase)
                messagebox.showinfo("Exitoso", "Producto añadido exitosamente!")
                
            self.default()
            self.update_table()
        except Exception as err:
            print(f"[-] save_purchase: {err}")
            messagebox.showerror("Error", f"Error al {"guardar" if self.band else "editar"} compra en BD")
        finally:
            self.band = None
    
    def get_purchase(self) -> None:
        selected = self.table.focus()
        if selected is None or selected == "":
            raise Exception("No se encontro la compra")
        
        values = self.table.item(selected, "values")
        self.enable_edit()
        self.opm_id.set(values[0])
        # FIXME: Ver que hacer con esta linea
        # self.opm_id.configure(state=DISABLED)
        self.opm_product.set(values[1])
        self.opm_supplier.set(self.suppliers[int(values[2])])
        self.tx_date.insert(0, values[3])
        self.tx_unitary_price.insert(0, values[4])
        self.tx_quantity.insert(0, values[5])
    
    def edit_purchase(self) -> None:
        try:
            self.get_purchase()
        except Exception as err:
            print("[-] ", err)
            messagebox.showinfo("._.", err)
            return
        
        self.band = False
    
    def _return(self) -> None:
        self.controller.show_frame("Menu")
    
    def clear_purchase(self):
        self.opm_id.configure(values=self.purchases)
        self.opm_id.set(self.purchases[0] if len(self.purchases) > 0 else "No disponible")
        self.opm_supplier.configure(values=list(self.suppliers.values()))
        self.opm_supplier.set(next(iter(self.suppliers.values())) if len(self.suppliers) > 0 else "No disponible")
        self.opm_product.configure(values=list(self.products.values()))
        self.opm_product.set(next(iter(self.products.values())) if len(self.products) > 0 else "No disponible")
        self.tx_quantity.delete(0, END)
        self.tx_unitary_price.delete(0, END)
        self.tx_date.delete(0, END)
        
    def default(self):
        # TODO: Actualizar los valores de los productos, proveedores y compras (Pensar cuales son necesarios)
        self.state(True)
        self.clear_purchase()
        self.bt_add.configure(state=ENABLE)
        self.bt_edit.configure(state=ENABLE)
        self.bt_new.configure(state=ENABLE)
        self.bt_save.configure(state=DISABLED)
        self.bt_cancel.configure(state=DISABLED)
        self.bt_remove.configure(state=ENABLE)
        self.state(False)
    
    def state(self, state: bool) -> None:
        self.opm_id.configure(state=ENABLE if state else DISABLED)
        self.opm_supplier.configure(state=ENABLE if state else DISABLED)
        self.opm_product.configure(state=ENABLE if state else DISABLED)
        self.tx_quantity.configure(state=ENABLE if state else DISABLED)
        self.tx_unitary_price.configure(state=ENABLE if state else DISABLED)
        self.tx_date.configure(state=ENABLE if state else DISABLED)
        
        
    def enable_edit(self):
        self.bt_new.configure(state=DISABLED)
        self.bt_save.configure(state=ENABLE)
        self.bt_cancel.configure(state=ENABLE)
        self.bt_edit.configure(state=DISABLED)
        self.bt_remove.configure(state=DISABLED)
        
        self.state(True)
        self.clear_purchase()
    
    def insert_table(self, data: list) -> None:
        for i, row in enumerate(data):
            self.table.insert("", "end", iid=i, values=row)
            
    def clear_table(self) -> None:
        self.table.delete(*self.table.get_children())
        
    def update_table(self) -> None:
        self.clear_table()
        detail_purchase = db_detail_purchase.get_detail_purchases_by_user_id(self, self.profile.get_id())
        if len(detail_purchase) < 1:
            messagebox.showwarning("No hay productos", "No hay productos disponibles")
        self.insert_table(detail_purchase)
    
    # def convert_supplier(self, list_supplier: list) -> list:
    #     aux = list()
    #     for L in list_supplier:
    #         L = list(L)
    #         L[8] = self.suppliers[L[8]]
    #         aux.append(L)
    #     return aux
    
    def validate(self) -> None:
        # Empty
        entry_empty(self.tx_date, "Fecha")
        entry_empty(self.tx_unitary_price, "Precio u.")
        entry_empty(self.tx_quantity, "Cantidad")
        
        if self.selected_purchase == "":
            raise Exception("Seleccione una compra")
        
        if self.selected_supplier == "":
            raise Exception("Seleccione un proveedor")
        
        if self.selected_product == "":
            raise Exception("Seleccione un producto")
        
        # Exist
        detail_purchase = detail_purchase_class(int(self.opm_id.get()), find_id(self.products, self.opm_product.get()))
        if self.band != False:
            if db_detail_purchase.search_bool(self, detail_purchase):
                raise Exception("El producto ya existe en esta compra")
        
        if self.selected_purchase == "No disponible":
            raise Exception("No hay compras disponibles")
        
        if self.selected_supplier == "No disponible":
            raise Exception("No hay proveedores disponibles")
        
        if self.selected_product == "No disponible":
            raise Exception("No hay productos disponibles")
        
        # Type
        if not self.opm_id.get().isdecimal():
            raise Exception("ID debe ser un número")
        
        if not self.tx_quantity.get().isdecimal():
            raise Exception("Cantidad debe ser un número entero")
        
        if not is_numeric(self.tx_unitary_price.get()):
            raise Exception("Precio unitario debe ser un número")
        
        if self.opm_supplier.get() not in list(self.suppliers.values()):
            raise Exception("El proveedor no esta listado")
        
        if self.opm_product.get() not in list(self.products.values()):
            raise Exception("El producto no esta listado")
        
        try:
            datetime.strptime(self.tx_date.get(), "%Y-%m-%d")
        except Exception as err:
            raise Exception(f"Fecha no valida: {err}")