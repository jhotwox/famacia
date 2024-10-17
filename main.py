from customtkinter import CTk, CTkFrame as Frame
from login import Login

class myApp(CTk):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
        self.config(width=400, height=400)
        self.title("FARMACIA")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        self.main_container = Frame(self)
        self.main_container.grid(padx=40, pady=40, sticky="nsew")
        
        self.shared_data = dict()
        
        # Todas las clases de frames
        self.frames = dict()
        
        self.frames["Login"] = Login(self.main_container, self)
        self.frames["Login"].grid(row=0, column=0, sticky="nsew")
        
        self.show_frame("Login")
        
    def show_frame(self, page_name) -> None:
        try:
            frame = self.frames[page_name]
            frame.tkraise()
        except Exception as err:
            print(f"[-] show_frame in myApp: {err}")
    
    def add_frame(self, page_name, frame_class, *args) -> None:
        if page_name not in self.frames:
            frame = frame_class(self.main_container, self, *args)
            frame.configure(width=600, height=400)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
    
root = myApp()
root.mainloop()