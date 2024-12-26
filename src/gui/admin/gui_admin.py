import customtkinter as ctk
from gui.admin.gui_project_frame import ProjectFrame
from gui.admin.gui_users_frame import UserFrame
from gui.admin.gui_admin_selected_frame import SelectedFrame
from gui.gui_appearance_color import appearance_color, get_default_styles
from features.feature_admin_event_handlers import EventHandlers
from tkinter import PhotoImage

class AdminGUI:
    
    def __init__(self, master, username, user_id):
        self.colors = appearance_color()
        self.styles = get_default_styles()
        self.master = master
        self.user_id = user_id
        
        # Fenster für den Admin
        self.master.geometry("1200x800")
        self.master.title("TimeArch - More Time for Visions")
        self.master.configure(bg=self.colors["background"])
        
        icon_path = "C:/Users/ricar/OneDrive/Dokumente/VS_Projects/Semesterprojekt_Zeiterfassungssystem/docs/Logo_TimeArch.ico"
        self.master.iconbitmap(icon_path)
        
        # Willkommen Label für den Admin
        welcome_text = f"Willkommen, Admin {username}!"
        welcome_label = ctk.CTkLabel(master=self.master, text = welcome_text, **self.styles["title"])
        welcome_label.grid(row=0, column=0, columnspan=4, pady=10, padx=10, sticky="nw")
        
        # Admin Frame in 4 columns aufteilen
        self.master.grid_columnconfigure(0, minsize=600, weight=0)
        self.master.grid_columnconfigure(1, minsize=600, weight=0)
        self.master.grid_columnconfigure(2, weight=2)
        self.master.grid_rowconfigure(1, weight=1)
 
        # Frames initialisieren
        self.project_frame = ProjectFrame(self.master)
        self.project_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
               
        self.users_frame = UserFrame(self.master)
        self.users_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        
        self.selected_frame = SelectedFrame(self.master, self.user_id, None, None)
        self.selected_frame.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")
        
        # Event-Handler initialisieren
        self.event_handlers = EventHandlers(self)
        
        # Binden der Doppelklick-Events
        self.users_frame.user_treeview.bind("<Double-Button-1>", self.event_handlers.on_user_double_click)
        self.project_frame.project_treeview.bind("<Double-Button-1>", self.event_handlers.on_project_double_click)
        
    def open_selected_frame(self, selected_id, selected_name, description=None):
        self.selected_frame.update_project_details(selected_id, selected_name, description)
        
    
def start_admin_gui(username, user_id):
    try:
        root = ctk.CTk()
        admin_gui = AdminGUI(root, username, user_id)
        root.mainloop()
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")