import customtkinter as ctk
from gui_project_frame import ProjectFrame
from gui_users_frame import UserFrame
from gui_appearance_color import appearance_color

class AdminGUI:
    
    def __init__(self, master, username):
        self.master = master
        appearance_color()
        
        # Fenster für den Admin
        self.master.title("Admin Interface")
        self.master.geometry("1200x800")
        
        welcome_text = f"Willkommen, Admin {username}!"
        welcome_label = ctk.CTkLabel(self.master, text = welcome_text, font=("", 20))
        welcome_label.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky="w")
        
        # Admin Frame in 5 columns aufteilen
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_columnconfigure(2, weight=3)
        self.master.rowconfigure(1, weight=1)
 
        # Frame für Projekte
        self.project_frame = ProjectFrame(self.master)
               
        # Frame für Users
        self.users_frame = UserFrame(self.master)
    
def start_admin_gui(username):
    try:
        root = ctk.CTk()
        admin_gui = AdminGUI(root, username)
        root.mainloop()
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")