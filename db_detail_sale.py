from tkinter import messagebox
import database as con
from detail_sale import detail_sale as detail_sale_class

table = "detail_sale"

class db_detail_sale:
    def save(self, detail_sale: detail_sale_class) -> None:
        try:
            self.conn = con.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"INSERT INTO {table}(sale_id, product_id, quantity, unitary_price) VALUES (%s,%s,%s,%s)"
            self.data = (
                detail_sale.get_sale_id(),
                detail_sale.get_product_id(),
                detail_sale.get_quantity(),
                detail_sale.get_unitary_price()
            )
            self.cursor.execute(self.sql, self.data)
            self.conn.commit()
        except Exception as err:
            print(f"[-] save: {err}")
            messagebox.showerror("Error", "Error al guardar detalle venta")
        finally:
            self.conn.close()
    
    def edit(self, detail_sale: detail_sale_class) -> None:
        try:
            self.conn = con.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"UPDATE {table} SET quantity=%s, unitary_price=%s WHERE sale_id={detail_sale.get_sale_id()} AND product_id={detail_sale.get_product_id()}"
            self.data = (
                detail_sale.get_quantity(),
                detail_sale.get_unitary_price()
            )
            self.cursor.execute(self.sql, self.data)
            self.conn.commit()
        except Exception as err:
            print(f"[-] edit_db_detail_sale: {err}")
            raise Exception(f"Error al editar detalle venta: {err}")
        finally:
            self.conn.close()

    def remove(self, detail_sale: detail_sale_class) -> None:
        try:
            self.conn = con.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"DELETE FROM {table} WHERE sale_id={detail_sale.get_sale_id()} AND product_id={detail_sale.get_product_id()}"
            self.cursor.execute(self.sql)
            self.conn.commit()
        except Exception as err:
            print(f"[-] remove in db_detail_sale: {err}")
            raise Exception(f"Error al eliminar detalle venta: {err}")
        finally:
            self.conn.close()
    
    def get_all_detail_sales(self) -> list:
        try:
            self.conn = con.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"SELECT * FROM {table}"
            self.cursor.execute(self.sql)
            rows = self.cursor.fetchall()
            self.conn.commit()
            self.conn.close()
            if rows is None:
                raise Exception("No se encontraron detalles de venta")
            return rows
        except Exception as err:
            print("[-] get_all_detail_sales: ", err)
            messagebox.showerror("Error", "Error en la consulta")
    
    def get_detail_sales_by_user_id(self, user_id: int) -> list:
        try:
            self.conn = con.conection().open()
            self.cursor = self.conn.cursor()
            
            self.sql = f"""
            SELECT sale.id, detail_sale.quantity, product.name, detail_sale.unitary_price, sale.discount, (detail_sale.unitary_price * detail_sale.quantity * (1 - sale.discount*0.01)) AS subtotal, ((detail_sale.unitary_price * detail_sale.quantity* (1 - sale.discount*0.01)) * 0.16) AS iva, ((detail_sale.unitary_price * detail_sale.quantity * (1 - sale.discount*0.01)) * 1.16) AS total
            FROM detail_sale, sale, product
            WHERE detail_sale.sale_id = sale.id AND detail_sale.product_id = product.id AND sale.id = {user_id}
            """
            self.cursor.execute(self.sql)
            
            rows = self.cursor.fetchall()
            self.conn.commit()
            self.conn.close()
            if rows is None:
                raise Exception("No se encontraron detalles venta")
            return rows
        except Exception as err:
            print("[-] get_detail_sales_by_user_id: ", err)
            messagebox.showerror("Error", "Error en la consulta")
            
    # def get_detail_sales_for_table_by_id(self) -> list:
    #     try:
    #         self.conn = con.conection().open()
    #         self.cursor = self.conn.cursor()
            
    #         # FIXME: Actualizar consulta
    #         ("ID", "Cantidad", "Nombre", "Precio u.", "Descuento", "Subtotal", "IVA", "Importe")
    #         self.sql = f"""
    #         SELECT sale.id, detail_sale.quantity, product.name, detail_sale.unitary_price, sale.discount, (detail_sale.unitary_price * detail_sale.quantity * (1 - sale.discount*0.01)) AS subtotal, ((detail_sale.unitary_price * detail_sale.quantity* (1 - sale.discount*0.01)) * 0.16) AS iva, ((detail_sale.unitary_price * detail_sale.quantity * (1 - sale.discount*0.01)) * 1.16) AS total FROM detail_sale, sale, product WHERE detail_sale.sale_id = sale.id AND detail_sale.product_id = product.id AND sale.id = {user_id}
    #         """
    #         self.cursor.execute(self.sql)
    #         rows = self.cursor.fetchall()
    #         self.conn.commit()
    #         self.conn.close()
    #         if rows is None:
    #             raise Exception("No se encontraron detalles venta")
    #         return rows
    #     except Exception as err:
    #         print("[-] get_detail_sales_by_user_id: ", err)
    #         messagebox.showerror("Error", "Error en la consulta")
            
    def search_bool(self, detail_sale: detail_sale_class) -> bool:
        try:
            self.conn = con.conection().open()
            self.cursor = self.conn.cursor()
            print("*-*-*-*-*-*-*-*-*-*-*")
            print("db_detail_sale")
            print(f"search_bool\nsale_id -> {detail_sale.get_sale_id()}\nproduct_id -> {detail_sale.get_product_id()}")
            print("*-*-*-*-*-*-*-*-*-*-*")
            self.sql = f"SELECT COUNT(*) FROM {table} WHERE sale_id={detail_sale.get_sale_id()} AND product_id={detail_sale.get_product_id()}"
            self.cursor.execute(self.sql)
            row = self.cursor.fetchone()
            self.conn.commit()
            return row[0]
        except Exception as err:
            print("[-] search_bool db_detail_sale: ", err)
            raise Exception("No se encontro el detalle de venta")
        finally:
            self.conn.close()

    def close(self):
        self.conn.close()