from tkinter import messagebox
import database as con
from customer import customer as customer_class
from db_functions import name_available, max_id

table = "customer"

class db_customer:
    def save(self, customer: customer_class) -> None:
        try:
            self.con = con.conection()
            self.conn = self.con.open()
            self.cursor = self.conn.cursor()
            name_available(customer.get_name(), table)
            self.sql = f"INSERT INTO {table}(id, name, points, adress, phone) VALUES (%s,%s,%s,%s,%s)"
            self.data = (
                customer.get_id(),
                customer.get_name(),
                customer.get_points(),
                customer.get_adress(),
                customer.get_phone()
            )
            self.cursor.execute(self.sql, self.data)
            self.conn.commit()
        except Exception as err:
            print(f"[-] save: {err}")
            messagebox.showerror("Error", "Error al guardar cliente")
        finally:
            self.conn.close()
    
    def edit(self, customer: customer_class) -> None:
        try:
            self.con = con.conection()
            self.conn = self.con.open()
            self.cursor = self.conn.cursor()
            self.sql = f"UPDATE {table} SET name=%s, points=%s, adress=%s, phone=%s WHERE id={customer.get_id()}"
            self.data = (
                customer.get_name(),
                customer.get_points(),
                customer.get_adress(),
                customer.get_phone()
            )
            self.cursor.execute(self.sql, self.data)
            self.conn.commit()
        except Exception as err:
            print(f"[-] edit_db_customer: {err}")
            raise Exception(f"Error al editar cliente: {err}")
        finally:
            self.conn.close()

    def remove(self, customer: customer_class) -> None:
        try:
            self.con = con.conection()
            self.conn = self.con.open()
            self.cursor = self.conn.cursor()
            self.sql = f"DELETE FROM {table} WHERE id={customer.get_id()}"
            self.cursor.execute(self.sql)
            self.conn.commit()
        except Exception as err:
            print(f"[-] remove in db_customer: {err}")
            raise Exception(f"Error al eliminar cliente: {err}")
        finally:
            self.conn.close()

    def get_max_id(self) -> int:
        return max_id(table)
    
    def get_all_customers(self) -> list:
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
                raise Exception("No se encontraron clientes")
            return rows
        except Exception as err:
            print("[-] get_all_customers: ", err)
            messagebox.showerror("Error", "Error en la consulta")
    
    def get_dict_customers(self) -> dict:
        try:
            self.conn = con.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"SELECT id, name FROM {table}"
            self.cursor.execute(self.sql)
            rows = self.cursor.fetchall()
            self.conn.commit()
            self.conn.close()
            if rows is None:
                raise Exception("No se encontraron clientes")
            return {row[0]: row[1] for row in rows}
        except Exception as err:
            print("[-] get_dict_customers: ", err)
            messagebox.showerror("Error", "Error en la consulta")
    
    def get_points_by_id(self, customer_id: int) -> int:
        try:
            self.conn = con.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"SELECT points FROM {table} WHERE id={customer_id}"
            self.cursor.execute(self.sql)
            points = self.cursor.fetchone()
            self.conn.commit()
            self.conn.close()
            if points is None:
                raise Exception("No se encontraron puntos")
            return points[0]
        except Exception as err:
            print("[-] get_points_by_id: ", err)
            messagebox.showerror("Error", "Error en la consulta")
    
    def close(self):
        self.conn.close()