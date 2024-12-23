import customtkinter as ctk
from tkinter import PhotoImage
from gui.user.gui_user_project_frame import UserProjectFrame
from gui.user.gui_user_selected_frame import UserSelectedFrame
from gui.gui_appearance_color import appearance_color, get_default_styles
from features.feature_user_event_handlers import UserEventHandlers

class UserGUI:
    
    def __init__(self, master, username, user_id):
        self.master = master
        self.username = username
        self.user_id = user_id
        colors = appearance_color()
        styles = get_default_styles()        
        
        # Fenster für den Admin
        self.master.geometry("1200x800")
        self.master.title("TimeArch - More Time for Visions")
        self.master.configure(bg=colors['background'])
        
        icon_image = PhotoImage(file=r"C:\Users\ricar\OneDrive\Dokumente\VS_Projects\Semesterprojekt_Zeiterfassungssystem\docs\Logo_TimeArch.gif")
        self.master.iconphoto(False, icon_image)

        
        # Willkommen Label für den Admin
        welcome_text = f"Willkommen, {username}!"
        welcome_label = ctk.CTkLabel(master=self.master, text = welcome_text, **styles["title"])
        welcome_label.grid(row=0, column=0, columnspan=3, pady=10, padx=10, sticky="nw")
        
        # Admin Frame in 4 columns aufteilen
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=2)
        self.master.grid_rowconfigure(1, weight=1)
        
        # Frames initialisieren
        self.user_project_frame = UserProjectFrame(self.master, self.username)
        self.user_project_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew" )
        
        self.selected_frame = UserSelectedFrame(self.master, self.user_id, None, None)
        self.selected_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        
        # Event-Handler initialisieren
        self.user_event_handlers = UserEventHandlers(self.user_project_frame, self.selected_frame)
        
        # Binden der Doppelklick-Events
        self.user_project_frame.project_treeview.bind("<Double-Button-1>", self.user_event_handlers.on_project_double_click)
        
    def open_selected_frame(self, selected_id, selected_name, description=None):
        self.selected_frame.update_project_details(selected_id, selected_name, description)
    
        
def start_user_gui(username, user_id):
    try:
        root = ctk.CTk()
        user_gui = UserGUI(root, username, user_id)
        root.mainloop()
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")