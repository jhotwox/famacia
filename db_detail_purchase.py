from tkinter import messagebox
import database as con
from detail_purchase import detail_purchase as detail_purchase_class

table = "detail_purchase"

class db_detail_purchase:
    def save(self, detail_purchase: detail_purchase_class) -> None:
        try:
            self.conn = con.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"INSERT INTO {table}(purchase_id, product_id, unitary_price, quantity) VALUES (%s,%s,%s,%s)"
            self.data = (
                detail_purchase.get_purchase_id(),
                detail_purchase.get_product_id(),
                detail_purchase.get_unitary_price(),
                detail_purchase.get_quantity()
            )
            self.cursor.execute(self.sql, self.data)
            self.conn.commit()
        except Exception as err:
            print(f"[-] save: {err}")
            messagebox.showerror("Error", "Error al guardar detalle compra")
        finally:
            self.conn.close()
    
    def edit(self, detail_purchase: detail_purchase_class) -> None:
        try:
            self.conn = con.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"UPDATE {table} SET unitary_price=%s, quantity=%s WHERE purchase_id={detail_purchase.get_purchase_id()} AND product_id={detail_purchase.get_product_id()}"
            self.data = (
                detail_purchase.get_unitary_price(),
                detail_purchase.get_quantity()
            )
            self.cursor.execute(self.sql, self.data)
            self.conn.commit()
        except Exception as err:
            print(f"[-] edit_db_detail_purchase: {err}")
            raise Exception(f"Error al editar detalle compra: {err}")
        finally:
            self.conn.close()

    def remove(self, detail_purchase: detail_purchase_class) -> None:
        try:
            self.conn = con.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"DELETE FROM {table} WHERE purchase_id={detail_purchase.get_purchase_id()} AND product_id={detail_purchase.get_product_id()}"
            self.cursor.execute(self.sql)
            self.conn.commit()
        except Exception as err:
            print(f"[-] remove in db_detail_purchase: {err}")
            raise Exception(f"Error al eliminar detalle compra: {err}")
        finally:
            self.conn.close()
    
    def get_all_detail_purchases(self) -> list:
        try:
            self.conn = con.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"SELECT * FROM {table}"
            self.cursor.execute(self.sql)
            rows = self.cursor.fetchall()
            self.conn.commit()
            self.conn.close()
            if rows is None:
                raise Exception("No se encontraron detalles compra")
            return rows
        except Exception as err:
            print("[-] get_all_detail_purchases: ", err)
            messagebox.showerror("Error", "Error en la consulta")
    
    def get_detail_purchases_by_user_id(self, user_id: int) -> list:
        try:
            self.conn = con.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"SELECT purchase.id, product.name, product.supplier, purchase.date, detail_purchase.unitary_price, detail_purchase.quantity, (detail_purchase.unitary_price * detail_purchase.quantity) AS total FROM detail_purchase, purchase, product, user WHERE detail_purchase.purchase_id = purchase.id AND detail_purchase.product_id = product.id AND user.id = purchase.user_id AND user.id = {user_id}"
            self.cursor.execute(self.sql)
            rows = self.cursor.fetchall()
            self.conn.commit()
            self.conn.close()
            if rows is None:
                raise Exception("No se encontraron detalles compra")
            return rows
        except Exception as err:
            print("[-] get_detail_purchases_by_user_id: ", err)
            messagebox.showerror("Error", "Error en la consulta")
            
    def search_bool(self, detail_purchase: detail_purchase_class) -> bool:
        try:
            self.conn = con.conection().open()
            self.cursor = self.conn.cursor()
            print("*-*-*-*-*-*-*-*-*-*-*")
            print("db_detail_purchase")
            print(f"search_bool\npurchase_id -> {detail_purchase.get_purchase_id()}\nproduct_id -> {detail_purchase.get_product_id()}")
            print("*-*-*-*-*-*-*-*-*-*-*")
            self.sql = f"SELECT COUNT(*) FROM {table} WHERE purchase_id={detail_purchase.get_purchase_id()} AND product_id={detail_purchase.get_product_id()}"
            self.cursor.execute(self.sql)
            row = self.cursor.fetchone()
            self.conn.commit()
            return row[0]
        except Exception as err:
            print("[-] search_bool db_detail_purchase: ", err)
            raise Exception("No se encontro el detalle de compra")
        finally:
            self.conn.close()

    def close(self):
        self.conn.close()