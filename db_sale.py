from tkinter import messagebox
import database as con
from sale import sale as sale_class
from db_functions import max_id

from user import user as user_class

table = "sale"

class db_sale:
    def save(self, sale: sale_class) -> None:
        try:
            self.conn = con.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"INSERT INTO {table}(id, customer_id, total, date, discount) VALUES (%s,%s,%s,%s,%s)"
            self.data = (
                sale.get_id(),
                sale.get_customer_id(),
                sale.get_total(),
                sale.get_date(),
                sale.get_discount()
            )
            self.cursor.execute(self.sql, self.data)
            self.conn.commit()
        except Exception as err:
            print(f"[-] save: {err}")
            messagebox.showerror("Error", "Error al guardar venta")
        finally:
            self.conn.close()
    
    def edit(self, sale: sale_class) -> None:
        try:
            self.con = con.conection()
            self.conn = self.con.open()
            self.cursor = self.conn.cursor()
            self.sql = f"UPDATE {table} SET customer_id=%s, total=%s, date=%s, discount=%s WHERE id={sale.get_id()}"
            self.data = (
                sale.get_customer_id(),
                sale.get_total(),
                sale.get_date(),
                sale.get_discount()
            )
            self.cursor.execute(self.sql, self.data)
            self.conn.commit()
        except Exception as err:
            print(f"[-] edit_db_sale: {err}")
            raise Exception(f"Error al editar venta: {err}")
        finally:
            self.conn.close()

    def remove(self, sale: sale_class) -> None:
        try:
            self.conn = con.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"DELETE FROM {table} WHERE id={sale.get_id()}"
            self.cursor.execute(self.sql)
            self.conn.commit()
        except Exception as err:
            print(f"[-] remove in db_sale: {err}")
            raise Exception(f"Error al eliminar venta: {err}")
        finally:
            self.conn.close()

    def get_max_id(self) -> int:
        return max_id(table)
    
    def get_all_sales_by_user(self, profile: user_class) -> list:
        try:
            self.conn = con.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"SELECT * FROM {table} WHERE user_id={profile.get_id()}"
            self.cursor.execute(self.sql)
            rows = self.cursor.fetchall()
            self.conn.commit()
            self.conn.close()
            if rows is None:
                raise Exception("No se encontraron ventas")
            return rows
        except Exception as err:
            print("[-] get_all_sales_by_user: ", err)
            messagebox.showerror("Error", "Error en la consulta")
    
    def get_id_sales(self, profile: user_class) -> list:
        try:
            self.conn = con.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"SELECT id FROM {table} WHERE user_id={profile.get_id()}"
            self.cursor.execute(self.sql)
            rows = self.cursor.fetchall()
            self.conn.commit()
            self.conn.close()
            if rows is None:
                raise Exception("No se encontraron ventas")
            return [str(row[0]) for row in rows]
        except Exception as err:
            print("[-] get_id_sales: ", err)
            messagebox.showerror("Error", "Error en la consulta")
    
    def count_detail_sales(self, sale: sale_class) -> int:
        try:
            self.conn = con.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"SELECT COUNT(*) FROM detail_sale WHERE sale_id={sale.get_id()}"
            self.cursor.execute(self.sql)
            rows = self.cursor.fetchone()
            self.conn.commit()
            self.conn.close()
            if rows is None:
                raise Exception("No se encontraron ventas")
            return rows[0]
        except Exception as err:
            print("[-] count_detail_sales: ", err)
            messagebox.showerror("Error", "Error en la consulta")
    
    def close(self):
        self.conn.close()