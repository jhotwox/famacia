from tkinter import messagebox
import database as con
from purchase import purchase as purchase_class
from db_functions import max_id
from user import user as user_class

table = "purchase"

class db_purchase:
    def save(self, purchase: purchase_class) -> None:
        try:
            self.conn = con.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"INSERT INTO {table}(id, date, total, user_id) VALUES (%s,%s,%s,%s)"
            self.data = (
                purchase.get_id(),
                purchase.get_date(),
                purchase.get_total(),
                purchase.get_user_id()
            )
            self.cursor.execute(self.sql, self.data)
            self.conn.commit()
        except Exception as err:
            print(f"[-] save: {err}")
            messagebox.showerror("Error", "Error al guardar compra")
        finally:
            self.conn.close()
    
    def edit(self, purchase: purchase_class) -> None:
        try:
            self.con = con.conection()
            self.conn = self.con.open()
            self.cursor = self.conn.cursor()
            self.sql = f"UPDATE {table} SET date=%s, total=%s WHERE id={purchase.get_id()}"
            self.data = (
                purchase.get_date(),
                purchase.get_total()
            )
            self.cursor.execute(self.sql, self.data)
            self.conn.commit()
        except Exception as err:
            print(f"[-] edit_db_purchase: {err}")
            raise Exception(f"Error al editar compra: {err}")
        finally:
            self.conn.close()

    def remove(self, purchase: purchase_class) -> None:
        try:
            self.conn = con.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"DELETE FROM {table} WHERE id={purchase.get_id()}"
            self.cursor.execute(self.sql)
            self.conn.commit()
        except Exception as err:
            print(f"[-] remove in db_purchase: {err}")
            raise Exception(f"Error al eliminar compra: {err}")
        finally:
            self.conn.close()

    def get_max_id(self) -> int:
        return max_id(table)
    
    def get_all_purchases(self, profile: user_class) -> list:
        try:
            self.conn = con.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"SELECT * FROM {table} WHERE user_id={profile.get_id()}"
            self.cursor.execute(self.sql)
            rows = self.cursor.fetchall()
            self.conn.commit()
            self.conn.close()
            if rows is None:
                raise Exception("No se encontraron compras")
            return rows
        except Exception as err:
            print("[-] get_all_purchases: ", err)
            messagebox.showerror("Error", "Error en la consulta")
    
    def get_id_purchases(self, profile: user_class) -> list:
        try:
            self.conn = con.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"SELECT id FROM {table} WHERE user_id={profile.get_id()}"
            self.cursor.execute(self.sql)
            rows = self.cursor.fetchall()
            self.conn.commit()
            self.conn.close()
            if rows is None:
                raise Exception("No se encontraron compras")
            return [str(row[0]) for row in rows]
        except Exception as err:
            print("[-] get_all_purchases: ", err)
            messagebox.showerror("Error", "Error en la consulta")
    
    def count_detail_purchase(self, purchase: purchase_class) -> int:
        try:
            self.conn = con.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"SELECT COUNT(*) FROM detail_purchase WHERE purchase_id={purchase.get_id()}"
            self.cursor.execute(self.sql)
            rows = self.cursor.fetchone()
            self.conn.commit()
            self.conn.close()
            if rows is None:
                raise Exception("No se encontraron compras")
            return rows[0]
        except Exception as err:
            print("[-] count_detail_purchase: ", err)
            messagebox.showerror("Error", "Error en la consulta")
    
    # def get_id_purchase(self, profile: user_class) -> list:
    #     try:
    #         self.conn = con.conection().open()
    #         self.cursor = self.conn.cursor()
    #         self.sql = f"SELECT id FROM {table} WHERE user_id={profile.get_id()}"
    #         self.cursor.execute(self.sql)
    #         rows = self.cursor.fetchall()
    #         self.conn.commit()
    #         self.conn.close()
    #         if rows is None:
    #             raise Exception("No se encontraron compras")
    #         return rows
    #     except Exception as err:
    #         print("[-] get_id_purchases: ", err)
    #         messagebox.showerror("Error", "Error en la consulta")
        
    
    def close(self):
        self.conn.close()