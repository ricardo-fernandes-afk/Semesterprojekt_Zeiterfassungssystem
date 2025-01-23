"""
Modul: Benutzer-GUI für TimeArch.

Dieses Modul stellt die grafische Benutzeroberfläche für die Benutzer bereit. Es ermöglicht Benutzern, ihre Projekte
anzuzeigen und auszuwählen sowie Details zu verwalten.

Klassen:
--------
- UserGUI: Hauptklasse für die Benutzer-GUI, die Frames für Projekte und Projektdetails integriert.

Methoden:
---------
- __init__(self, master, username, user_id): Initialisiert die GUI mit Benutzername und Benutzer-ID.
- open_selected_frame(self, selected_id, selected_name, description=None): Öffnet den Frame mit den Details des ausgewählten Projekts.
- on_closing(self): Schließt die Anwendung und zerstört das Fenster.

Funktionen:
-----------
- start_user_gui(username, user_id): Startet die Benutzer-GUI in einem neuen Fenster.

Verwendung:
-----------
    from gui_users import start_user_gui

    start_user_gui(username="John Doe", user_id=1)
"""

import customtkinter as ctk
from tkinter import PhotoImage
from gui.user.gui_user_project_frame import UserProjectFrame
from gui.user.gui_user_selected_frame import UserSelectedFrame
from gui.gui_appearance_color import appearance_color, get_default_styles
from features.feature_user_event_handlers import UserEventHandlers

class UserGUI:
    """
    Hauptklasse für die Benutzer-GUI.

    Funktionen:
    - Anzeige der Benutzerprojekte in einem Treeview.
    - Anzeige von Projekt-Details bei Auswahl.
    - Integration von Ereignis-Handlern für Benutzerinteraktionen.
    """
    def __init__(self, master, username, user_id):
        """
        Initialisiert die GUI mit Benutzername und Benutzer-ID.

        Args:
            master (ctk.CTk): Das übergeordnete Fenster.
            username (str): Der Benutzername des aktuellen Benutzers.
            user_id (int): Die ID des aktuellen Benutzers.
        """
        self.master = master
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.username = username
        self.user_id = user_id
        colors = appearance_color()
        styles = get_default_styles()        
        
        # Fenster für den Admin
        self.master.geometry("1200x800")
        self.master.title("TimeArch - More Time for Visions")
        self.master.configure(bg=colors['background'])
        
        icon_path = "C:/Users/ricar/OneDrive/Dokumente/VS_Projects/Semesterprojekt_Zeiterfassungssystem/docs/Logo_TimeArch.ico"
        self.master.iconbitmap(icon_path)

        # Willkommen Label für den Admin
        welcome_text = f"Willkommen, {username}!"
        welcome_label = ctk.CTkLabel(master=self.master, text = welcome_text, **styles["title"])
        welcome_label.grid(row=0, column=0, columnspan=3, pady=10, padx=10, sticky="nw")
        
        # Admin Frame in 4 columns aufteilen
        self.master.grid_columnconfigure(0, minsize=600, weight=0)
        self.master.grid_columnconfigure(1, weight=3)
        self.master.grid_rowconfigure(1, weight=1)
        
        # Frames initialisieren
        self.user_project_frame = UserProjectFrame(self.master, self.username)
        self.user_project_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew" )
        
        self.selected_frame = UserSelectedFrame(self.master, self.user_id, self.username, None, None)
        self.selected_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        
        # Event-Handler initialisieren
        self.user_event_handlers = UserEventHandlers(self.user_project_frame, self.selected_frame)
        
        # Binden der Doppelklick-Events
        self.user_project_frame.project_treeview.bind("<Double-Button-1>", self.user_event_handlers.on_project_double_click)
        
    def open_selected_frame(self, selected_id, selected_name, description=None):
        """
        Öffnet den Frame mit den Details des ausgewählten Projekts.

        Args:
            selected_id (str): Die Projektnummer oder ID des ausgewählten Eintrags.
            selected_name (str): Der Name des ausgewählten Eintrags.
            description (str, optional): Die Beschreibung des Projekts. Standard ist None.
        """
        self.selected_frame.update_project_details(selected_id, selected_name, description)
    
    def on_closing(self):
        """
        Schließt die Anwendung und zerstört das Fenster.
        """
        self.master.destroy()    
        
def start_user_gui(username, user_id):
    """
    Startet die Benutzer-GUI in einem neuen Fenster.

    Args:
        username (str): Der Benutzername.
        user_id (int): Die Benutzer-ID.

    Fehlerbehandlung:
    ------------------
    - Gibt eine Fehlermeldung aus, falls ein Fehler beim Start der GUI auftritt.
    """
    try:
        root = ctk.CTk()
        user_gui = UserGUI(root, username, user_id)
        root.mainloop()
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
    
