from customtkinter import END, CTkButton as Button, CTkEntry as Entry, CTkLabel as Label, DISABLED, NORMAL as ENABLE, CTkFrame as Frame, CTkOptionMenu as OptMenu, StringVar, CTkScrollbar as Scrollbar
from tkinter import messagebox
from tkinter.ttk import Treeview
from functions import entry_empty, find_id, is_numeric, get_datetime, print_time
from table_style import apply_style
from db_functions import get_unitary_price_by_id, get_supplier_by_purchase_id
from sale import sale as sale_class
from detail_sale import detail_sale as detail_sale_class
from db_sale import db_sale
from db_detail_sale import db_detail_sale
from datetime import datetime

from db_product import db_product
from user import user as user_class
from db_customer import db_customer

class Sales(Frame):
    def __init__(self, container, controller, profile: user_class, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        
        # Constants
        self.EDITAR = 0
        self.NUEVO = 1
        
        #  Global parameters
        self.controller = controller
        self.profile = profile
        
        # Flags
        self.band = None
        self.search_band = False
        self.new_sale_state = 0 # 0: "Nuevo", 1: productos == 0, 2: "Pagar" (productos >= 1), 3: "Comprar"
        # Products no tiene nada que ver con opm_product
        
        self.products = db_product.get_dict_products(self)
        
        fr_search = Frame(self)
        fr_search.grid(row=0, column=0, sticky="nsw", padx=10, pady=10)
        fr_entry = Frame(self)
        fr_entry.grid(row=1, column=0, sticky="nsw", padx=10, pady=10)
        fr_table = Frame(self)
        fr_table.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        fr_button = Frame(self)
        fr_button.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)
        
        lb_search_sale = Label(fr_search, text="ID venta", font=("Calisto MT", 12))
        lb_search_sale.grid(row=0, column=0, padx=5)
        self.id_sales = db_sale.get_id_sales(self)
        # print("ID Purchases -> ", self.id_purchases)
        self.selected_search_sale = StringVar(value=self.id_sales[0] if len(self.id_sales) > 0 else "No disponible")
        self.opm_search_sale = OptMenu(fr_search, values=self.id_sales, variable=self.selected_search_sale)
        self.opm_search_sale.grid(row=0, column=1, padx=10, pady=10)
        
        self.bt_search = Button(fr_search, text="Buscar", border_width=2, width=100, command=self.search_sale)
        self.bt_search.grid(row=0, column=2, padx=5, pady=10)
        
        #region Row 0
        self.categories = db_product.get_category(self)
        lb_category = Label(fr_entry, text="Categoria")
        lb_category.grid(row=0, column=0, pady=0, sticky="w")
        self.selected_category = StringVar(value=self.categories[0] if len(self.categories) > 0 else "No disponible")
        self.selected_category.trace("w", self.on_selection_category)
        self.opm_category = OptMenu(fr_entry, values=self.categories, variable=self.selected_category)
        self.opm_category.grid(row=0, column=1, pady=5)
        
        self.sales = self.id_sales.copy()
        lb_id = Label(fr_entry, text="ID")
        lb_id.grid(row=0, column=2, pady=0, sticky="w")
        self.selected_sale = StringVar(value=self.sales[0] if len(self.sales) > 0 else "No disponible")
        self.selected_sale.trace("w", self.on_selection_sale)
        self.opm_id = OptMenu(fr_entry, values=self.sales, variable=self.selected_sale)
        self.opm_id.grid(row=0, column=3, pady=5)
        
        #region Row 1
        lb_product = Label(fr_entry, text="Producto")
        lb_product.grid(row=1, column=0, pady=0, sticky="w")
        self.selected_product = StringVar(value="No disponible")
        self.opm_product = OptMenu(fr_entry, values=list(), variable=self.selected_product)
        self.opm_product.grid(row=1, column=1, pady=5)
        
        self.customers = db_customer.get_dict_customers(self)
        lb_customer = Label(fr_entry, text="Cliente")
        lb_customer.grid(row=1, column=2, pady=0, sticky="w")
        self.selected_customer = StringVar(value="No disponible")
        self.selected_customer.trace("w", self.on_selection_customer)
        self.opm_customer = OptMenu(fr_entry, values=list(self.customers.values()), variable=self.selected_customer)
        self.opm_customer.grid(row=1, column=3, pady=5)
        
        #region Row 2
        lb_quantity = Label(fr_entry, text="Cantidad")
        lb_quantity.grid(row=2, column=0, pady=0, sticky="w")
        self.tx_quantity = Entry(fr_entry, placeholder_text="Cantidad")
        self.tx_quantity.grid(row=2, column=1, pady=5, padx=20)
        
        lb_points = Label(fr_entry, text="Puntos")
        lb_points.grid(row=2, column=2, pady=0, sticky="w")
        self.tx_points = Entry(fr_entry, placeholder_text="Puntos")
        self.tx_points.grid(row=2, column=3, pady=5, padx=20)
        
        lb_pay = Label(fr_entry, text="Pago")
        lb_pay.grid(row=3, column=0, pady=0, sticky="w")
        self.tx_pay = Entry(fr_entry, placeholder_text="Pago")
        self.tx_pay.grid(row=3, column=1, pady=5, padx=20)
        
        #region Table
        self.table_columns = ("ID", "Cantidad", "Nombre", "Precio u.", "Descuento", "Subtotal", "IVA", "Importe")
        
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
        
        self.table['columns'] = self.table_columns
        self.table.column("#0", width=0, stretch=False)
        self.table.column(self.table_columns[0], anchor="center", width=30) # ID
        self.table.column(self.table_columns[1], anchor="center", width=70) # Cantidad
        self.table.column(self.table_columns[2], anchor="center", width=150) # Nombre
        self.table.column(self.table_columns[3], anchor="center", width=80) # Precio u.
        self.table.column(self.table_columns[4], anchor="center", width=85) # Descuento
        self.table.column(self.table_columns[5], anchor="center", width=80) # Subtotal
        self.table.column(self.table_columns[6], anchor="center", width=80) # IVA
        self.table.column(self.table_columns[7], anchor="center", width=80) # Importe
        
        self.table.heading("#0", text="", anchor="center")
        self.table.heading(self.table_columns[0], text=self.table_columns[0], anchor="center")
        self.table.heading(self.table_columns[1], text=self.table_columns[1], anchor="center")
        self.table.heading(self.table_columns[2], text=self.table_columns[2], anchor="center")
        self.table.heading(self.table_columns[3], text=self.table_columns[3], anchor="center")
        self.table.heading(self.table_columns[4], text=self.table_columns[4], anchor="center")
        self.table.heading(self.table_columns[5], text=self.table_columns[5], anchor="center")
        self.table.heading(self.table_columns[6], text=self.table_columns[6], anchor="center")
        self.table.heading(self.table_columns[7], text=self.table_columns[7], anchor="center")
        
        self.bt_add = Button(fr_button, text="Añadir producto", border_width=1, width=60, command=self.add_product)
        self.bt_add.grid(row=0, column=0, padx=5, pady=10)
        self.bt_new = Button(fr_button, text="Nueva venta", border_width=1, width=60, command=self.new_sale)
        self.bt_new.grid(row=0, column=1, padx=5, pady=10)
        self.bt_edit = Button(fr_button, text="Editar", border_width=1, width=60, command=self.edit_product)
        self.bt_edit.grid(row=0, column=2, padx=5, pady=10)
        self.bt_remove = Button(fr_button, text="Eliminar", border_width=1, width=60, command=self.remove_product)
        self.bt_remove.grid(row=0, column=3, padx=5, pady=10)
        self.bt_cancel = Button(fr_button, text="Cancelar compra", border_width=1, width=60, command=self.cancel_sale)
        self.bt_cancel.grid(row=0, column=4, padx=5, pady=10)
        self.bt_clean = Button(fr_button, text="Limpiar", border_width=1, width=60, command=self.default)
        self.bt_clean.grid(row=0, column=5, padx=5, pady=10)
        self.bt_return = Button(fr_button, text="Regresar", border_width=1, width=60, command=self._return)
        self.bt_return.grid(row=0, column=6, padx=5, pady=10)
        
        self.default()
    
    # region on_selection
    def on_selection_category(self, *args):
        if self.band == self.EDITAR:
            return
        
        products = db_product.get_dict_products_by_category(self, self.selected_category.get())
        self.opm_product.configure(values=list(products.values()))
        self.opm_product.set(next(iter(products.values())) if len(products) > 0 else "No disponible")
        return
    
    def on_selection_sale(self, *args):
        return
    
    def on_selection_customer(self, *args):
        # print("Selected customer -> ", self.selected_customer.get())
        if self.selected_customer.get() != "" and self.selected_customer.get() != "No disponible":
            self.tx_points.configure(state=ENABLE)
            self.tx_points.delete(0, END)
            customer_id = find_id(self.customers, self.selected_customer.get())
            points = db_customer.get_points_by_id(self, customer_id)
            self.tx_points.insert(0, points)
            self.tx_points.configure(state=DISABLED)
    
    # region search
    def search_sale(self):
        self.search_band = True
        return
    
    # region add_product
    def add_product(self):
        try:
            self.validate_new_product()
        except Exception as err:
            print("[-] add_product_validation: ", err)
            messagebox.showwarning("Error >_<", err)
            return
        
        try:
            # ("ID✅", "Cantidad✅", "Nombre✅", "Precio u.❌", "Descuento❌", "Subtotal✅", "IVA✅", "Importe✅")
            # Obtener información que falta
            product_id = find_id(self.products, self.selected_product.get())
            (unitary_price, discount) = db_product.unitary_price_and_discount(self, product_id)
            percentage = str(discount)+"%"
            
            # Ya existe el producto en la tabla
            table_id = self.search_name_table(self.selected_product.get())
            if table_id is not None:
                current_quantity = int(self.table.item(table_id, "values")[1])
                new_quantity = current_quantity + int(self.tx_quantity.get())
                # Validar stock disponible
                stock = db_product.get_stock_by_id(self, product_id)
                if new_quantity > stock:
                    raise Exception(f"No hay suficiente stock de este producto\nStock: {stock}")
                
                subtotal = (unitary_price * new_quantity) * (1 - discount)
                self.table.set(table_id, column="Cantidad", value=new_quantity)
                self.table.set(table_id, column="Subtotal", value=subtotal)
                self.table.set(table_id, column="IVA", value=subtotal * 0.16)
                self.table.set(table_id, column="Importe", value=subtotal * 1.16)
                self.delete_last_row()
                self.insert_total()
                return
            
            # No existe el producto en la tabla
            id = int(self.selected_sale.get())
            quantity = int(self.tx_quantity.get())
            name = self.selected_product.get()
            discount = discount*0.01
            subtotal = (unitary_price * quantity)*(1-discount)
            iva = subtotal * 0.16
            amount = subtotal + iva
            
            product = [id, quantity, name, unitary_price, percentage, subtotal, iva, amount]
            if self.new_sale_state == 2:
                self.delete_last_row()
            self.insert_new_row(product)
            self.insert_total()
            if self.new_sale_state == 1:
                self.new_sale_state = 2
                self.opm_customer.configure(state=DISABLED)
            
        except Exception as err:
            print("[-] add_product: ", err)
            messagebox.showwarning("Error >_<", err)
            return
    
    # region new_sale
    def new_sale(self):
        if self.new_sale_state == 0:
            self.new_sale_new()
        elif self.new_sale_state == 1:
            self.new_sale_pay()
        elif self.new_sale_state == 3:
            self.new_sale_buy()
    
    def new_sale_new(self):
        self.state(True)
        self.clear_sale()
        self.clear_table()
        self.new_sale_state = 1
        self.bt_new.configure(text="Pagar")
        self.opm_id.set(db_sale.get_max_id(self)+1)
        self.opm_id.configure(state=DISABLED)
        
        # States
        self.bt_search.configure(state=DISABLED)
        self.tx_pay.configure(state=DISABLED)
        self.bt_add.configure(state=ENABLE)
        self.bt_edit.configure(state=ENABLE)
        self.bt_remove.configure(state=ENABLE)
        self.bt_cancel.configure(state=DISABLED)
        # clean y return siempre activos
    
    def new_sale_pay(self):
        if not self.table.get_children():
            messagebox.showwarning("Advertencia OoO", "No hay productos en la lista")
            return
        
        self.state(False)
        self.new_sale_state = 2
        self.bt_new.configure(text="Comprar")
        self.bt_clean.configure(text="Cancelar")
        
        # States
        self.tx_pay.configure(state=ENABLE)
        self.bt_add.configure(state=DISABLED)
        self.bt_edit.configure(state=DISABLED)
        # clean y return siempre activos    
    
    def new_sale_buy(self):
        if(self.tx_pay.get() == ""):
            messagebox.showerror("Error", "Ingrese el pago")
            return
        # Comprobar pago con total
        # Crear venta
        # Crear detalle venta
        # Actualizar puntos
        # Actualizar stock

        # COMPROBAR QUE SE PUEDE RESCATAR DE LA IA
        # self.state(False)
        # self.new_sale_state = 0
        # self.bt_new.configure(text="Nueva venta")
        # self.bt_clean.configure(text="Limpiar")
        
        # # States
        # self.bt_search.configure(state=ENABLE)
        # self.bt_add.configure(state=DISABLED)
        # self.bt_edit.configure(state=DISABLED)
        # self.bt_remove.configure(state=DISABLED)
        # self.bt_cancel.configure(state=ENABLE)
        # self.bt_clean.configure(state=ENABLE)
        # self.bt_return.configure(state=ENABLE)
    
    # region edit
    def edit_product(self):
        return
    
    # region remove
    def remove_product(self):
        return
    
    # region cancel
    def cancel_sale(self):
        return
    
    # region default
    def default(self):
        self.id_sales = db_sale.get_id_sales(self)
        self.state(True)
        self.clear_sale()
        self.clear_table()
        
        self.bt_search.configure(state=ENABLE)
        self.bt_add.configure(state=DISABLED)
        self.bt_new.configure(state=ENABLE)
        self.bt_edit.configure(state=DISABLED)
        self.bt_remove.configure(state=DISABLED)
        self.bt_cancel.configure(state=DISABLED)
        self.bt_clean.configure(state=ENABLE)
        self.bt_return.configure(state=ENABLE)
        self.bt_new.configure(text="Nueva venta")
        self.bt_add.configure(text="Añadir producto")
        self.state(False)
        self.band = None
        self.new_sale_state = 0
        self.search_band = False
    
    # region state
    def state(self, state: bool) -> None:
        self.opm_category.configure(state=ENABLE if state else DISABLED)
        self.opm_id.configure(state=ENABLE if state else DISABLED)
        self.opm_product.configure(state=ENABLE if state else DISABLED)
        self.opm_customer.configure(state=ENABLE if state else DISABLED)
        self.tx_quantity.configure(state=ENABLE if state else DISABLED)
        self.tx_points.configure(state=ENABLE if state else DISABLED)
        self.tx_pay.configure(state=ENABLE if state else DISABLED)
    
    # region clear
    def clear_sale(self):
        self.opm_category.set(self.categories[0] if len(self.categories) > 0 else "No disponible")
        self.opm_id.configure(values=self.id_sales)
        self.opm_id.set(self.id_sales[0] if len(self.id_sales) > 0 else "No disponible")
        self.opm_product.configure(values=list())
        self.opm_product.set("No disponible")
        self.opm_customer.set(next(iter(self.customers.values())) if len(self.customers) > 0 else "No disponible")
        self.tx_quantity.delete(0, END)
        self.tx_points.delete(0, END)
        self.tx_pay.delete(0, END)
    
    def clear_table(self):
        self.table.delete(*self.table.get_children())
        # for i in self.table.get_children():
        #     self.table.delete(i)
    
    def insert_table(self, data: list) -> None:
        for i, row in enumerate(data):
            self.table.insert("", "end", iid=i, values=row)
    
    def insert_new_row(self, data: list) -> None:
        self.table.insert("", "end", iid=len(self.table.get_children()), values=data)
    
    def delete_last_row(self) -> None:
        self.table.delete(self.table.get_children()[-1])
    
    def calculate_total(self):
        total = 0
        for row in self.table.get_children():
            total += float(self.table.item(row)["values"][-1])
        return total
    
    def insert_total(self):
        total = self.calculate_total()
        self.table.insert("", "end", values=["", "", "", "", "", "", "Total", total])
    
    def search_name_table(self, name) -> str | None:
        for item in self.table.get_children():
            item_values = self.table.item(item, "values")
            if item_values[2] == name:
                return item
        return None
    
    # region validate
    def validate_new_product(self):
        # Empty
        entry_empty(self.tx_quantity, "Cantidad")
        self.tx_points.configure(state=ENABLE)
        entry_empty(self.tx_points, "Cantidad")
        self.tx_points.configure(state=DISABLED)
        
        # Exist
        if self.selected_category.get() == "":
            raise Exception("Seleccione una categoria")
        
        if self.selected_category.get() == "No disponible":
            raise Exception("No hay categorias disponibles")
        
        if self.selected_sale.get() == "":
            raise Exception("Seleccione una venta")
        
        if self.selected_product.get() == "":
            raise Exception("Seleccione un producto")

        if self.selected_product.get() == "No disponible":
            raise Exception("No hay productos disponibles")
        
        if self.selected_customer.get() == "":
            raise Exception("Seleccione un cliente")
        
        # Type
        if not self.tx_quantity.get().isdecimal():
            raise Exception("La cantidad debe ser un número entero")
        
        self.tx_points.configure(state=ENABLE)
        if not self.tx_points.get().isdecimal():
            raise Exception("Los puntos deben ser un número entero")
        self.tx_points.configure(state=DISABLED)
        
        # Stock
        stock = db_product.get_stock_by_id(self, find_id(self.products, self.selected_product.get()))
        if int(self.tx_quantity.get()) > stock:
            raise Exception(f"No hay suficiente stock de este producto\nStock: {stock}")

    def _return(self):
        self.controller.show_frame("Menu")