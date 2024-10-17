from tkinter import messagebox
import mysql.connector as mysql

class conection:
    def __init__(self):
        self.user = "root"
        self.password = "OroJim11."
        self.database = "farmacia"
        self.host = "localhost"
        
    def open(self):
        try:
            self.conn = mysql.connect(
                host=self.host,
                user=self.user,
                passwd=self.password,
                database=self.database,
                charset='utf8mb4',
                collation='utf8mb4_general_ci'
            )
            return self.conn
        except mysql.Error as err:
            print(f"Error -> {err}")
            messagebox.showerror("DB Error", f"{err}")
            return None
    
    def close(self):
        self.conn.close()