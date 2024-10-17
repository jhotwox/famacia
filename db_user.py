from tkinter import messagebox
import mysql.connector as mysql
import database as con
from user import user as user_class
from db_functions import max_id

table = "user"

class db_user:    
    def save(self, user: user_class) -> None:
        self.con = con.conection()
        self.conn = self.con.open()
        self.cursor1 = self.conn.cursor()
        self.sql = f"INSERT INTO {table}(id, name, username, password, profile) values (%s,%s,%s,%s,%s)"
        self.data = (
            user.get_id(),
            user.get_name(),
            user.get_username(),
            user.get_password(),
            user.get_profile()
        )
        self.cursor1.execute(self.sql, self.data)
        self.conn.commit()
        self.conn.close()
        
    # def search(self, user: user_class) -> user_class:
    #     try:
    #         self.con = con.conection()
    #         self.conn = self.con.open()
    #         self.cursor1 = self.conn.cursor()
    #         aux = None
    #         self.sql = f"SELECT * FROM {table} WHERE id={user.get_id()}"
    #         self.cursor1.execute(self.sql)
    #         row = self.cursor1.fetchone()
    #         self.conn.commit()
    #         self.conn.close()
    #         if row[0] is not None:
    #             aux = user_class(int(row[0]), row[1], row[2], row[3], row[4])
    #     except:
    #         messagebox.showerror("Error", "No se encontro el usuario")
    #     return aux
    
    def edit(self, user: user_class) -> None:
        try:
            self.con = con.conection()
            self.conn = self.con.open()
            self.cursor1 = self.conn.cursor()
            self.sql = f"UPDATE {table} SET name=%s, username=%s, profile=%s, password=%s WHERE id={user.get_id()}"
            self.data = (
                user.get_name(),
                user.get_username(),
                user.get_profile(),
                user.get_password()
            )
            self.cursor1.execute(self.sql, self.data)
            self.conn.commit()
        except Exception as err:
            print(f"[-] edit in db_user: {err}")
            raise Exception(f"Error al editar usuario: {err}")
        finally:
            self.conn.close()
        
    def remove(self, user: user_class) -> None:
        try:
            self.con = con.conection()
            self.conn = self.con.open()
            self.cursor1 = self.conn.cursor()
            self.sql = f"DELETE FROM {table} WHERE id={user.get_id()}"
            self.cursor1.execute(self.sql)
            self.conn.commit()
        except Exception as err:
            print(f"[-] remove in db_user: {err}")
            raise Exception(f"Error al eliminar usuario: {err}")
        finally:
            self.conn.close()
        
    def get_max_id(self) -> int:
        return max_id(table)
    
    def get_all_users(self) -> list:
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
                raise Exception("No se encontraron usuarios")
            return rows
        except Exception as err:
            print("[-] get_all_users: ", err)
            messagebox.showerror("Error", "Error en la consulta")
        
    def authenticate(self, user: user_class) -> user_class:
        try:
            self.con = con.conection()
            self.conn = self.con.open()
            self.cursor1 = self.conn.cursor()
            self.sql = f"SELECT * FROM {table} WHERE username='{user.get_username()}'"
            self.cursor1.execute(self.sql)
            row = self.cursor1.fetchone()
            self.conn.commit()
            self.conn.close()
            if row is not None:
                if user.get_password() == row[3]:
                    return user_class(int(row[0]), row[1], row[2], row[3], row[4])
                else:
                    messagebox.showwarning("Error", "La contraseña no coincide")
            else:
                messagebox.showwarning("Error", "No se encontro el username")
            return None
        except mysql.Error as err:
            print(f"[-] Mysql: {err}")
            messagebox.showerror("DB Error", f"Error en la BD")
        except Exception as err:
            print(f"[-] {err}")
            messagebox.showerror("Error", f"Error al autenticar")
            return None
    
    def close(self):
        self.conn.close()