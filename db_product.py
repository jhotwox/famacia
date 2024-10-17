from tkinter import messagebox
import database as con
from product import product as product_class
from db_functions import name_available, max_id

table = "product"

class db_product:
    def save(self, product: product_class) -> None:
        try:
            self.con = con.conection()
            self.conn = self.con.open()
            self.cursor = self.conn.cursor()
            name_available(product.get_name(), table)
            self.sql = f"INSERT INTO {table}(id, name, description, sale_price, purchase_price, discount_sale, stock, category, supplier) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            self.data = (
                product.get_id(),
                product.get_name(),
                product.get_description(),
                product.get_sale_price(),
                product.get_purchase_price(),
                product.get_discount_sale(),
                product.get_stock(),
                product.get_category(),
                product.get_supplier()
            )
            self.cursor.execute(self.sql, self.data)
            self.conn.commit()
        except Exception as err:
            print(f"[-] save: {err}")
            messagebox.showerror("Error", "Error al guardar producto")
        finally:
            self.conn.close()
    
    def edit(self, product: product_class) -> None:
        try:
            self.con = con.conection()
            self.conn = self.con.open()
            self.cursor = self.conn.cursor()
            self.sql = f"UPDATE {table} SET name=%s, description=%s, sale_price=%s, purchase_price=%s, discount_sale=%s, stock=%s, category=%s, supplier=%s WHERE id={product.get_id()}"
            self.data = (
                product.get_name(),
                product.get_description(),
                product.get_sale_price(),
                product.get_purchase_price(),
                product.get_discount_sale(),
                product.get_stock(),
                product.get_category(),
                product.get_supplier()
            )
            self.cursor.execute(self.sql, self.data)
            self.conn.commit()
        except Exception as err:
            print(f"[-] edit_db_product: {err}")
            raise Exception(f"Error al editar producto: {err}")
        finally:
            self.conn.close()

    def remove(self, product: product_class) -> None:
        try:
            self.con = con.conection()
            self.conn = self.con.open()
            self.cursor = self.conn.cursor()
            self.sql = f"DELETE FROM {table} WHERE id={product.get_id()}"
            self.cursor.execute(self.sql)
            self.conn.commit()
        except Exception as err:
            print(f"[-] remove in db_product: {err}")
            raise Exception(f"Error al eliminar producto: {err}")
        finally:
            self.conn.close()

    def get_max_id(self) -> int:
        return max_id(table)
    
    def get_all_products(self) -> list:
        try:
            self.con = con.conection()
            self.conn = self.con.open()
            self.cursor = self.conn.cursor()
            aux = None
            self.sql = f"SELECT * FROM {table}"
            self.cursor.execute(self.sql)
            rows = self.cursor.fetchall()
            self.conn.commit()
            self.conn.close()
            if rows is None:
                raise Exception("No se encontraron productos")
            return rows
        except Exception as err:
            print("[-] get_all_products: ", err)
            messagebox.showerror("Error", "Error en la consulta")
    
    def get_dict_products(self) -> dict:
        try:
            self.conn = con.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"SELECT id, name FROM {table}"
            self.cursor.execute(self.sql)
            rows = self.cursor.fetchall()
            self.conn.commit()
            self.conn.close()
            if rows is None:
                raise Exception("No se encontraron productos")
            return {item[0]: item[1] for item in rows}
        except Exception as err:
            print("[-] get_dict_products: ", err)
            messagebox.showerror("Error", "Error en la consulta")
    
    def get_supplier_products(self, supplier_id: int) -> list:
        try:
            self.conn = con.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"SELECT * FROM product WHERE supplier={supplier_id}"
            self.cursor.execute(self.sql)
            rows = self.cursor.fetchall()
            self.conn.commit()
            self.conn.close()
            if rows is None:
                raise Exception("No se encontraron productos")
            return rows
        except Exception as err:
            print("[-] get_all_products: ", err)
            messagebox.showerror("Error", "Error en la consulta")
            
    def get_dict_products_by_supplier(self, supplier_id: int) -> dict:
        try:
            self.conn = con.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"SELECT id, name FROM {table} where supplier={supplier_id}"
            self.cursor.execute(self.sql)
            rows = self.cursor.fetchall()
            self.conn.commit()
            self.conn.close()
            if rows is None:
                raise Exception("No se encontraron productos")
            return {item[0]: item[1] for item in rows}
        except Exception as err:
            print("[-] get_dict_products_by_supplier: ", err)
            messagebox.showerror("Error", "Error en la consulta")
    
    def close(self):
        self.conn.close()