from tkinter import messagebox
import database as con
from supplier import supplier as supplier_class
from db_functions import name_available, max_id

table = "supplier"

class db_supplier:
    def save(self, supplier: supplier_class) -> None:
        try:
            self.con = con.conection()
            self.conn = self.con.open()
            self.cursor1 = self.conn.cursor()
            name_available(supplier.get_name(), table)
            self.sql = f"INSERT INTO {table}(id,  phone, name, address, bank_code) VALUES (%s,%s,%s,%s,%s)"
            self.data = (
                supplier.get_id(),
                supplier.get_phone(),
                supplier.get_name(),
                supplier.get_address(),
                supplier.get_bank_code()
                )
            self.cursor1.execute(self.sql, self.data)
            self.conn.commit()
        except Exception as err:
            print(f"[-] save: {err}")
            messagebox.showerror("Error", "Error al guardar proveedor")
            raise err
        finally:
            self.conn.close()
    
    def edit(self, supplier: supplier_class) -> None:
        try:
            self.con = con.conection()
            self.conn = self.con.open()
            self.cursor1 = self.conn.cursor()
            
            self.sql = f"UPDATE {table} SET phone=%s, name=%s, address=%s, bank_code=%s WHERE id={supplier.get_id()}"
            self.data = (
                supplier.get_phone(),
                supplier.get_name(),
                supplier.get_address(),
                supplier.get_bank_code()
                )
            self.cursor1.execute(self.sql, self.data)
            self.conn.commit()
        except Exception as err:
            print(f"[-] edit_db_supplier: {err}")
            raise Exception(f"Error al editar proveedor: {err}")
        finally:
            self.conn.close()

    def remove(self, supplier: supplier_class) -> None:
        try:
            self.con = con.conection()
            self.conn = self.con.open()
            self.cursor1 = self.conn.cursor()
            self.sql = f"DELETE FROM {table} WHERE id={supplier.get_id()}"
            self.cursor1.execute(self.sql)
            self.conn.commit()
        except Exception as err:
            print(f"[-] remove in db_supplier: {err}")
            raise Exception(f"Error al eliminar proveedor: {err}")
        finally:
            self.conn.close()

    def get_max_id(self) -> int:
        return max_id(table)
    
    def get_all_suppliers(self) -> list:
        try:
            self.con = con.conection()
            self.conn = self.con.open()
            self.cursor1 = self.conn.cursor()
            self.sql = f"SELECT id, name, bank_code, address, phone FROM {table}"
            self.cursor1.execute(self.sql)
            rows = self.cursor1.fetchall()
            self.conn.commit()
            self.conn.close()
            if rows is None:
                raise Exception("No se encontraron proveedores")
            return rows
        except Exception as err:
            print("[-] get_all_suppliers: ", err)
            messagebox.showerror("Error", "Error en la consulta")
    
    def get_suppliers(self) -> dict:
        try:
            self.conn = con.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"SELECT id, name FROM {table}"
            self.cursor.execute(self.sql)
            rows = self.cursor.fetchall()
            self.conn.commit()
            self.conn.close()
            if rows is None:
                raise Exception("No se encontraron proveedores")
            return {row[0]: row[1] for row in rows}
        except Exception as err:
            print("[-] get_all_suppliers: ", err)
            raise err
    
    def close(self):
        self.conn.close()