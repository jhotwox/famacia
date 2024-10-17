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
            self.cursor1 = self.conn.cursor()
            name_available(customer.get_name(), table)
            self.sql = f"INSERT INTO {table}(id, name, points, adress, phone) VALUES (%s,%s,%s,%s,%s)"
            self.data = (
                customer.get_id(),
                customer.get_name(),
                customer.get_points(),
                customer.get_adress(),
                customer.get_phone()
            )
            self.cursor1.execute(self.sql, self.data)
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
            self.cursor1 = self.conn.cursor()
            self.sql = f"UPDATE {table} SET name=%s, points=%s, adress=%s, phone=%s WHERE id={customer.get_id()}"
            self.data = (
                customer.get_name(),
                customer.get_points(),
                customer.get_adress(),
                customer.get_phone()
            )
            self.cursor1.execute(self.sql, self.data)
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
            self.cursor1 = self.conn.cursor()
            self.sql = f"DELETE FROM {table} WHERE id={customer.get_id()}"
            self.cursor1.execute(self.sql)
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
            self.cursor1 = self.conn.cursor()
            aux = None
            self.sql = f"SELECT * FROM {table}"
            self.cursor1.execute(self.sql)
            rows = self.cursor1.fetchall()
            self.conn.commit()
            self.conn.close()
            if rows is None:
                raise Exception("No se encontraron clientes")
            return rows
        except Exception as err:
            print("[-] get_all_customers: ", err)
            messagebox.showerror("Error", "Error en la consulta")
    
    def close(self):
        self.conn.close()