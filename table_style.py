from tkinter.ttk import Style

def apply_style():
    style = Style()
    style.theme_use("default")
    
    style.configure(
        "Custom.Treeview",
        background="#2E2E2E",
        foreground="#FFF",
        rowheight=25,
        fieldbackground="#2E2E2E"
    )
    style.configure(
        "Custom.Treeview.Heading",
        background="#1F1F1F",
        foreground="#FFF",
        font=("Arial", 12, "bold"),
    )
    style.map(
        "Custom.Treeview", 
        background=[("selected", "#3E65C5")],
        foreground=[("selected", "#FFF")]
    )
    style.map(
        "Custom.Treeview.Heading",
        background=[("active", "#FFF")],
        foreground=[("active", "#1F1F1F")]
    )