import customtkinter as ctk
from gui_project_frame import ProjectFrame
from gui_appearance_color import appearance_color

class AdminGUI:
    
    def __init__(self, master, username):
        self.master = master
        appearance_color()
        
        # Fenster für den Admin
        self.master.title("Admin Interface")
        self.master.geometry("1200x800")
        
        welcome_text = f"Willkommen, Admin {username}!"
        ctk.CTkLabel(self.master, text = welcome_text, font=("", 20)).grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky="w")
        
        # Frame für Projekte
        self.project_frame = ProjectFrame(self.master)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=4)
        self.master.rowconfigure(1, weight=1)
    
def start_admin_gui(username):
    root = ctk.CTk()
    admin_gui = AdminGUI(root, username)
    root.mainloop()