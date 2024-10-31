from customtkinter import END, CTkButton as Button, CTkEntry as Entry, CTkLabel as Label, DISABLED, NORMAL as ENABLE, CTkFrame as Frame, CTkOptionMenu as OptMenu, StringVar, CTkScrollbar as Scrollbar
from tkinter import messagebox
from tkinter.ttk import Treeview
from functions import entry_empty, find_id, get_datetime, print_time
from table_style import apply_style
from sale import sale as sale_class
from detail_sale import detail_sale as detail_sale_class
from db_sale import db_sale
from db_detail_sale import db_detail_sale

from db_product import db_product
from user import user as user_class
from db_customer import db_customer

class Sales(Frame):
    def __init__(self, container, controller, profile: user_class, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        
        #  Global parameters
        self.controller = controller
        self.profile = profile
        
        # Flags
        self.band: int = 1
        self.search_band = False
        self.new_sale_state = 0 # 0: "Nuevo", 1: productos == 0, 2: "Pagar" (productos >= 1), 3: "Comprar"
        self.discount = False
        self.edit_sale_state = 0 # 0: Se presiono el boton "Guardar" 1: Se presiono el boton "Confirmar" 
        
        self.products = db_product.get_dict_products(self)
        self.query_list = list()
        
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
        # self.selected_sale.trace("w", self.on_selection_sale)
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
        if self.band == 0:
            return
        
        products = db_product.get_dict_products_by_category(self, self.selected_category.get())
        self.opm_product.configure(values=list(products.values()))
        self.opm_product.set(next(iter(products.values())) if len(products) > 0 else "No disponible")

    def on_selection_customer(self, *args):
        # if self.search_band == 1:
            # print("[~]on_selection_customer omited: search_band -> ", self.search_band)
            # return
        
        if self.selected_customer.get() == "" or self.selected_customer.get() == "No disponible":
            # print("[~]on_selection_customer omited: customer value: -> ", self.selected_customer.get())
            return
        
        self.tx_points.configure(state=ENABLE)
        self.tx_points.delete(0, END)
        customer_id = find_id(self.customers, self.selected_customer.get())
        points = db_customer.get_points_by_id(self, customer_id)
        self.tx_points.insert(0, points)
        self.tx_points.configure(state=DISABLED)
        # Flag discount
        self.discount = points >= 50
    
    # region search
    def search_sale(self):
        if (self.selected_search_sale.get() == "" or self.selected_search_sale.get() == "No disponible"):
            messagebox.showwarning("Advertencia", "No se ha seleccionado ninguna venta a buscar")
            return
        
        self.search_band = True
        self.clear_sale()
        
        (name, points) = db_sale.get_customer_by_sale_id(self, int(self.selected_search_sale.get()))
        # print("sale_id -> ", self.selected_search_sale.get())
        # print("customer_name -> ", name)
        # print("points -> ", points)
        self.opm_id.configure(state=ENABLE)
        self.opm_customer.configure(state=ENABLE)
        # self.tx_points.configure(state=ENABLE)
        
        self.opm_id.set(self.selected_search_sale.get())
        self.selected_sale.set(self.selected_search_sale.get())
        self.opm_customer.set(name)
        self.selected_customer.set(name)
        # self.tx_points.delete(0, END)
        # self.tx_points.insert(0, points)
        
        self.opm_id.configure(state=DISABLED)
        self.opm_customer.configure(state=DISABLED)
        # self.tx_points.configure(state=DISABLED)
        
        rows = db_detail_sale.get_detail_sales_by_user_id(self, int(self.selected_search_sale.get()))
        self.insert_table(rows)
        self.insert_total()
        
        # States
        self.opm_category.configure(state=ENABLE)
        self.opm_product.configure(state=ENABLE)
        self.tx_quantity.configure(state=ENABLE)
        
        self.bt_search.configure(state=DISABLED)
        self.bt_add.configure(state=ENABLE)
        self.bt_new.configure(text="Guardar")
        self.bt_edit.configure(state=ENABLE)
        self.bt_remove.configure(state=ENABLE)
        self.bt_cancel.configure(state=ENABLE)
    
    # region add_product
    def add_product_edit(self):
        try:
            table_id = self.search_name_table(self.selected_product.get())
            if table_id is not None:
                product_id = find_id(self.products, self.selected_product.get())
                stock = db_product.get_stock_by_id(self, product_id)
                if int(self.tx_quantity.get()) > stock:
                    raise Exception(f"No hay suficiente stock de este producto\nStock: {stock}")
                
                unitary_price = float(self.table.item(table_id, "values")[3])
                discount = float(self.table.item(table_id, "values")[4].replace("%", ""))
                discount = discount*0.01
                subtotal = round((unitary_price * int(self.tx_quantity.get())) * (1 - discount), 2)
                self.table.set(table_id, column="Cantidad", value=self.tx_quantity.get())
                self.table.set(table_id, column="Subtotal", value=subtotal)
                self.table.set(table_id, column="IVA", value=round(subtotal * 0.16, 2))
                self.table.set(table_id, column="Importe", value=round(subtotal * 1.16, 2))
                self.delete_last_row()
                self.insert_total()
                
                # Se esta editando un producto que existe
                if self.search_band == True:
                    detail_product = detail_sale_class(
                        sale_id=int(self.selected_sale.get()),
                        product_id=product_id,
                        quantity=int(self.tx_quantity.get()),
                        unitary_price=unitary_price
                    )
                    self.query_list.append(["EDIT", detail_product])
        
        except Exception as err:
            print("[-] add_product_edit: ", err)
            raise Exception(err)
        finally:
            self.bt_add.configure(text="Añadir producto")
            self.bt_remove.configure(state=ENABLE)
            self.bt_new.configure(state=ENABLE)
            self.opm_category.configure(state=ENABLE)
            self.opm_product.configure(state=ENABLE)
            self.band = 1
    
    def add_product(self):
        # Give access to "cajero" profile
        if self.search_band == True:
            if self.controller.shared_data["VALIDATE"] == False and self.profile.get_profile() == "cajero":
                self.controller.show_frame("Login_Manager")
                return
        
        # Validate
        try:
            self.validate_new_product()
        except Exception as err:
            print("[-] add_product_validation: ", err)
            messagebox.showwarning("Error >_<", err)
            return
        
        try:
        # EDITAR
            if self.band == 0:
                self.add_product_edit()
                return
        except Exception as err:
            print("[-] add_product edit: ", err)
            messagebox.showwarning("Error >_<", err)
            return

        try:
        # AÑADIR
            # Obtener información que falta y descuento
            product_id = find_id(self.products, self.selected_product.get())
            (unitary_price, discount) = db_product.unitary_price_and_discount(self, product_id)
            if self.discount:
                discount = 50
            if self.search_band == True:
                if not self.table_is_empty():
                    discount = self.table.item(self.table.get_children()[0], "values")[4]
                    discount = int(discount.replace("%", ""))
                    print("Discount from table -> ", discount)
            percentage = str(discount)+"%"
        except Exception as err:
            print("[-] add_product calculate discount: ", err)
            messagebox.showwarning("Error >_<", err)
            return
            
        try:
            # Ya existe el producto en la tabla
            table_id = self.search_name_table(self.selected_product.get())
            if table_id is not None:
                current_quantity = int(self.table.item(table_id, "values")[1])
                new_quantity = current_quantity + int(self.tx_quantity.get())
                
                # Validar stock disponible
                stock = db_product.get_stock_by_id(self, product_id)
                if new_quantity > stock:
                    raise Exception(f"No hay suficiente stock de este producto\nStock: {stock}")
                
                discount = discount*0.01
                subtotal = round((unitary_price * new_quantity) * (1 - discount), 2)
                self.table.set(table_id, column="Cantidad", value=new_quantity)
                self.table.set(table_id, column="Subtotal", value=subtotal)
                self.table.set(table_id, column="IVA", value=round(subtotal * 0.16, 2))
                self.table.set(table_id, column="Importe", value=round(subtotal * 1.16, 2))
                self.delete_last_row()
                self.insert_total()
                
                # Se añadio stock a un producto que ya existe
                if self.search_band == True:
                    detail_product = detail_sale_class(
                        sale_id=int(self.selected_sale.get()),
                        product_id=product_id,
                        quantity=new_quantity,
                        unitary_price=unitary_price
                    )
                    self.query_list.append(["EDIT", detail_product])
                return
        except Exception as err:
            print("[-] add_product it's already on the table: ", err)
            messagebox.showwarning("Error >_<", err)
            return
        
        try:
            # No existe el producto en la tabla
            id = int(self.selected_sale.get())
            quantity = int(self.tx_quantity.get())
            name = self.selected_product.get()
            discount = discount*0.01
            subtotal = round((unitary_price * quantity)*(1-discount), 2)
            iva = round(subtotal * 0.16, 2)
            amount = round(subtotal + iva, 2)
            
            # product row
            product = [id, quantity, name, unitary_price, percentage, subtotal, iva, amount]
            
            # Delete total row if exists
            # if self.new_sale_state == 2 or self.sea:
            if not self.table_is_empty():
                self.delete_last_row()
            
            # Insert new row
            print("After insert new row")
            self.insert_new_row(product)
            print("Before insert new row")
            self.insert_total()
            print("Before insert total")
            
            if self.search_band == True:
                detail_product = detail_sale_class(
                    sale_id=id,
                    product_id=product_id,
                    quantity=quantity,
                    unitary_price=unitary_price
                )
                self.query_list.append(["SAVE", detail_product])
            
            # If table is empty update state
            if self.new_sale_state == 1:
                self.new_sale_state = 2
                self.opm_customer.configure(state=DISABLED)
        except Exception as err:
            print("[-] add_product it's not in the table: ", err)
            messagebox.showwarning("Error >_<", err)
    
    # region new_sale
    def new_sale(self):
        # Boton guardar compra
        if self.search_band == True:
            # Give access to "cajero" profile
            if self.controller.shared_data["VALIDATE"] == False and self.profile.get_profile() == "cajero":
                self.controller.show_frame("Login_Manager")
                return
            
            print("edit_sale_state: ", self.edit_sale_state)
            if self.edit_sale_state == 0:
                self.bt_new.configure(text="Confirmar")
                self.state(False)
                self.opm_customer.configure(state=ENABLE)
                self.edit_sale_state = 1
            elif self.edit_sale_state == 1:
                self.edit_existing_sale()
            else:
                print("[-] Estado de edición desconocido: ", self.edit_sale_state, "Posibles valores: 0 - 2")
            return
        
        if self.new_sale_state == 0: # Nuevo
            self.new_sale_new()
        elif self.new_sale_state == 1:
            messagebox.showwarning("Advertencia OoO", "No hay productos en la lista")
        elif self.new_sale_state == 2: # Pagar
            self.new_sale_pay()
        elif self.new_sale_state == 3: # Comprar
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
        self.new_sale_state = 3
        self.bt_new.configure(text="Comprar")
        self.bt_clean.configure(text="Cancelar")
        
        # States
        self.tx_pay.configure(state=ENABLE)
        self.bt_add.configure(state=DISABLED)
        self.bt_edit.configure(state=DISABLED)
        # clean y return always active
    
    def new_sale_buy(self):
        # Validate
        try:
            self.validate_buy()
        except Exception as err:
            print("[-]")
            messagebox.showwarning("Error >.<", err)
            return
        
        # Comprobar que pago sea suficiente
        print("Before get total")
        total = self.get_total()
        print("total -> ", total)
        change = float(self.tx_pay.get()) - total
        print("Cambio -> ", change)
        if change < 0:
            messagebox.showerror("Error", "El pago no es suficiente\n Faltan: $"+str(-change))
            return
        
        self.state (False)
        
        try:
            # Crear venta
            sale = sale_class(
                id=int(self.selected_sale.get()),
                customer_id=find_id(self.customers, self.selected_customer.get()),
                total=round(total, 2),
                date=get_datetime(),
                discount=50 if self.discount else 0
            )
            db_sale.save(self, sale)
            print("Venta creada")
            
            # Obtener todas las filas de la tabla
            rows = self.obtain_rows_table()
            
            # Crear detalle venta
            print(rows)
            self.save_detail_sale(rows)
            
            # Actualizar puntos
            points = 0
            # print("Discount -> ", self.discount)
            if self.discount == False:
                points = self.calculate_points(total)
            
            customer_id = find_id(self.customers, self.selected_customer.get())
            # print("customer_id -> ", customer_id)
            customer = db_customer.get_customer_by_id(self, customer_id)
            if self.discount:
                customer.set_points(0)
            else:
                customer.set_points(customer.get_points() + points)
            
            # print("customer points -> ", customer.get_points())
            db_customer.edit(self, customer)
            
            # Actualizar banderas y estados (Cambiar el estado aqui para que no cambie el funcionamiento del boton clean)
            messagebox.showinfo("Venta exitosa", "Cambio: $"+str(change)+"\nPuntos obtenidos: "+str(points))
            self.new_sale_state = 0
            self.discount = False
            self.default()
        
        except Exception as err:
            print("[-] new_sale_buy: ", err)
            messagebox.showerror("Error >_<", err)
    
    def get_sale(self) -> None:
        selected = self.table.focus()
        if selected is None or selected == "":
            raise Exception("No se encontro el producto")
        
        values = self.table.item(selected, "values")
        
        if values[-2] == "Total":
            messagebox.showinfo(">_<", "No se puede editar el total")
            return
        
        self.state(False)
        self.opm_product.configure(state=ENABLE)
        self.tx_quantity.configure(state=ENABLE)
        
        self.opm_product.set(values[2])
        self.selected_product.set(values[2])
        self.tx_quantity.delete(0, END)
        self.tx_quantity.insert(0, values[1])
        
        self.opm_product.configure(state=DISABLED)
    
    # region edit
    def edit_product(self):
        
        # Give access to "cajero" profile
        if self.search_band == True:
            if self.controller.shared_data["VALIDATE"] == False and self.profile.get_profile() == "cajero":
                self.controller.show_frame("Login_Manager")
                return
        
        try:
            self.get_sale()
            self.band = 0
            self.bt_add.configure(text="Guardar")
            self.bt_remove.configure(state=DISABLED)
            self.bt_new.configure(state=DISABLED)
        except Exception as err:
            print("[-] edit_product: ", err)
            messagebox.showerror("Error", "No se logro editar el producto")
    
    def edit_existing_sale(self):
        # query list
        # save, edit, remove detail_sale
        if self.query_list is None or self.query_list == dict():
            print("Query list empty")
        else:
            try:
                for item in self.query_list:
                    if item[0] == "SAVE":
                        db_detail_sale.save(self, item[1])
                    elif item[0] == "EDIT":
                        db_detail_sale.edit(self, item[1])
                    elif item[0] == "REMOVE":
                        db_detail_sale.remove(self, item[1])
                    else:
                        raise Exception(f"Invalid Query: [{item[0]}, {item[1]}]")
            except Exception as err:
                print("[-] edit_existing_sale query_list: ", err)
                messagebox.showerror("Error >_<", err)
                return
        
        # Edit sale
        customer_id = find_id(self.customers, self.selected_customer.get())
        total = self.get_total()
        sale_id = self.selected_sale.get()
        aux = db_sale.get_sale_by_id(self, sale_id)
        sale = sale_class(
            sale_id,
            customer_id,
            total,
            aux.get_date(),
            discount=aux.get_discount()
        )
        try:
            db_sale.edit(self, sale)
        except Exception as err:
            print("[-]edit_existing_sale db_sale.edit(): ", err)
            messagebox.showerror("Error >_<", err)
            return
        
        messagebox.showinfo("0u0", "Venta editada correctamente!")
        self.default()
    
    # region remove
    def remove_product(self):
        # Give access to "cajero" profile
        if self.search_band == True:
            if self.controller.shared_data["VALIDATE"] == False and self.profile.get_profile() == "cajero":
                self.controller.show_frame("Login_Manager")
                return
        
        try:
            selected = self.table.focus()
            if selected is None or selected == "":
                messagebox.showinfo(">_<", "No se selecciono un producto")
                return
            
            values = self.table.item(selected, "values")
            
            if values[-2] == "Total":
                messagebox.showinfo(">_<", "No se puede eliminar el total")
                return
            
            self.table.delete(selected)
            
            # Update total
            self.delete_last_row()
            if self.table.get_children():
                self.insert_total()
            else:
                self.new_sale_state = 1
            
            if self.search_band == True:
                product_id = find_id(self.products, values[2])
                detail_product = detail_sale_class(
                    sale_id=int(values[0]),
                    product_id=product_id
                )
                self.query_list.append(["REMOVE", detail_product])
            
        except Exception as err:
            print("[-] remove_product: ", err)
            messagebox.showerror("Error", "No se logro eliminar el producto")
    
    # region cancel
    def cancel_sale(self):
        # Give access to "cajero" profile
        if self.search_band == True:
            if self.controller.shared_data["VALIDATE"] == False and self.profile.get_profile() == "cajero":
                self.controller.show_frame("Login_Manager")
                return
        
        try:
            sale_id = int(self.selected_search_sale.get())
            db_detail_sale.remove_by_sale_id(self, sale_id)
            sale = sale_class(id=sale_id)
            db_sale.remove(self, sale)
            messagebox.showinfo(">u<", "Venta cancelada")
            self.default()
        except Exception as err:
            print("[-] cancel_sale: ", err)
            messagebox.showerror("Error", "No se logro cancelar la venta")
    
    def obtain_rows_table(self) -> list:
        rows = []
        for item in self.table.get_children():
            rows.append(self.table.item(item)["values"])
        return rows[:-1]
    
    def save_detail_sale(self, rows: list) -> None:
        try:
            for row in rows:
                detail_sale = detail_sale_class(
                    sale_id=row[0],
                    product_id=find_id(self.products, row[2]),
                    quantity=row[1],
                    unitary_price=row[3],
                )
                db_detail_sale.save(self, detail_sale)
        except Exception as err:
            print("[-] save_detail_sale: ", err)
            raise Exception("Error al guardar el detalle de la venta")
    
    def calculate_points(self, total: float) -> int:
        points = 0
        if total >= 500:
            points = int(total // 100)
        return points
    
    # region default
    def default(self) -> None:        
        if self.new_sale_state == 3:
            self.new_sale_state = 2
            self.state(True)
            self.bt_new.configure(text="Pagar")
            self.bt_clean.configure(text="Limpiar")
            self.tx_pay.delete(0, END)
            # States
            self.opm_id.configure(state=DISABLED)
            self.bt_search.configure(state=DISABLED)
            self.tx_pay.configure(state=DISABLED)
            self.bt_add.configure(state=ENABLE)
            self.bt_edit.configure(state=ENABLE)
            self.bt_remove.configure(state=ENABLE)
            self.bt_cancel.configure(state=DISABLED)
            return
        
        self.id_sales = db_sale.get_id_sales(self)
        self.opm_search_sale.configure(values=self.id_sales)
        self.opm_search_sale.set(self.id_sales[0] if len(self.id_sales) > 0 else "No disponible")
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
        self.bt_clean.configure(text="Limpiar")
        self.state(False)
        self.band = 1
        self.new_sale_state = 0
        self.edit_sale_state = 0
        self.search_band = False
        self.query_list = list()
        self.controller.shared_data["VALIDATE"] = False
    
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
    
    def clear_table(self) -> None:
        self.table.delete(*self.table.get_children())
    
    def insert_table(self, data: list) -> None:
        for i, row in enumerate(data):
            self.table.insert("", "end", iid=i, values=row)
    
    def insert_new_row(self, data: list) -> None:
        # Se modifico debido a un error en la inserción de la fila al añadir un producto que fue eliminado previamente y se volvio a añadir (probado con una venta existente)
        # self.table.insert("", "end", iid=len(self.table.get_children()), values=data)
        self.table.insert("", "end", values=data)
    
    def delete_last_row(self) -> None:
        self.table.delete(self.table.get_children()[-1])
    
    def calculate_total(self) -> float:
        total = 0
        for row in self.table.get_children():
            total += float(self.table.item(row)["values"][-1])
        return total
    
    def get_total(self) -> float:
        return float(self.table.item(self.table.get_children()[-1], "values")[-1])

    def table_is_empty(self) -> bool:
        return self.table.get_children() is None or self.table.get_children() == ()
     
    # No se usa
    def total_row_exist(self) -> bool:
        return self.table.item(self.table.get_children()[-1], "values")[-2] == "Total"
    
    def insert_total(self) -> None:
        total = self.calculate_total()
        if total >= 500:
            self.table.insert("", "end", values=["", "", "", "", "", "10%", "Total", total*0.9])
        else:
            self.table.insert("", "end", values=["", "", "", "", "", "", "Total", total])
    
    def search_name_table(self, name) -> str | None:
        for item in self.table.get_children():
            item_values = self.table.item(item, "values")
            if item_values[2] == name:
                return item
        return None
    
    # region validate
    def validate_new_product(self) -> None:
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

    def validate_buy(self) -> None:
        if(self.tx_pay.get() == ""):
            raise Exception("Ingrese el pago")
        
        try:
            float(self.tx_pay.get())
        except:
            raise Exception("El pago debe ser un número")
    
    def _return(self) -> None:
        self.controller.shared_data["VALIDATE"] = False
        self.controller.show_frame("Menu")