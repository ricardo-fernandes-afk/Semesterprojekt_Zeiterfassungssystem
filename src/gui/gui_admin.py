import customtkinter as ctk
from gui.gui_project_frame import ProjectFrame
from gui.gui_users_frame import UserFrame
from gui.gui_appearance_color import appearance_color

class AdminGUI:
    
    def __init__(self, master, username):
        self.master = master
        appearance_color()
        
        # Fenster für den Admin
        self.master.title("Admin Interface")
        self.master.geometry("1200x800")
        
        # Willkommen Label für den Admin
        welcome_text = f"Willkommen, Admin {username}!"
        welcome_label = ctk.CTkLabel(master=self.master, text = welcome_text, font=("", 20))
        welcome_label.grid(row=0, column=0, columnspan=4, pady=10, padx=10, sticky="nw")
        
        # Admin Frame in 4 columns aufteilen
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_columnconfigure(2, weight=2)
        self.master.grid_columnconfigure(3, weight=2)
        self.master.grid_rowconfigure(1, weight=1)
 
        # Frame für Projekte
        self.project_frame = ProjectFrame(self.master)
        self.project_frame.grid(row=1, column=0, columnspan=1, padx=10, pady=10, sticky="nsew")
               
        # Frame für Users
        self.users_frame = UserFrame(self.master)
        self.users_frame.grid(row=1, column=1, columnspan=1, padx=10, pady=10, sticky="nsew")
    
def start_admin_gui(username):
    try:
        root = ctk.CTk()
        admin_gui = AdminGUI(root, username)
        root.mainloop()
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")