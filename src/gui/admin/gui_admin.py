"""
Modul: Admin-GUI für TimeArch.

Dieses Modul erstellt die grafische Benutzeroberfläche (GUI) für Administratoren. Es ermöglicht die Verwaltung von Projekten,
Benutzern und ausgewählten Projektdetails in einem dreispaltigen Layout. Ereignis-Handler ermöglichen Interaktionen
wie Doppelklicks auf Projekte oder Benutzer.

Klassen:
--------
- AdminGUI: Stellt die Haupt-Admin-GUI bereit, einschließlich aller Frames und Ereignis-Handler.

Funktionen:
-----------
- __init__(self, master, username, user_id): Initialisiert die Admin-GUI mit dem Hauptfenster, dem Benutzernamen und der Benutzer-ID.
- open_selected_frame(self, selected_id, selected_name, description=None): Öffnet den Frame für das ausgewählte Projekt.
- on_closing(self): Schließt das Fenster und beendet die Anwendung.
- start_admin_gui(username, user_id): Startet die Admin-GUI in einem neuen Fenster.

Verwendung:
-----------
    from gui_admin import start_admin_gui

    start_admin_gui("Admin", 1)
"""

import customtkinter as ctk
from gui.admin.gui_project_frame import ProjectFrame
from gui.admin.gui_users_frame import UserFrame
from gui.admin.gui_admin_selected_frame import SelectedFrame
from gui.gui_appearance_color import appearance_color, get_default_styles
from features.feature_admin_event_handlers import EventHandlers
from features.get_resource_path import get_resource_path
from tkinter import PhotoImage

class AdminGUI:
    """
    Klasse für die Haupt-GUI für Administratoren.

    Diese Klasse erstellt das Hauptfenster für Administratoren mit drei Frames:
    - `ProjectFrame`: Zeigt die Projektliste an.
    - `UserFrame`: Zeigt die Benutzerliste an.
    - `SelectedFrame`: Zeigt Details des ausgewählten Projekts an.
    """
    def __init__(self, master, username, user_id):
        """
        Initialisiert die Admin-GUI mit dem Hauptfenster, dem Benutzernamen und der Benutzer-ID.

        Args:
            master (ctk.CTk): Das Hauptfenster.
            username (str): Der Benutzername des Admins.
            user_id (int): Die ID des Admin-Benutzers.
        """
        self.master = master
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.colors = appearance_color()
        self.styles = get_default_styles()
        self.user_id = user_id
        self.icon_path = get_resource_path("src/Logo_TimeArch.ico")
        
        # Fenster für den Admin
        self.master.geometry("1200x800")
        self.master.title("TimeArch - More Time for Visions")
        self.master.configure(bg=self.colors["background"])
        
        self.master.iconbitmap(self.icon_path)
        
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
        """
        Öffnet den Frame für das ausgewählte Projekt und zeigt dessen Details an.

        Args:
            selected_id (str): Die Projektnummer oder Benutzer-ID des ausgewählten Eintrags.
            selected_name (str): Der Name des ausgewählten Eintrags (Projekt oder Benutzer).
            description (str, optional): Die Beschreibung des ausgewählten Projekts.
        """
        self.selected_frame.update_project_details(selected_id, selected_name, description)
    
    def on_closing(self):
        """
        Schließt das Fenster und beendet die Anwendung.
        """
        self.master.destroy()
        
    
def start_admin_gui(username, user_id):
    """
    Startet die Admin-GUI in einem neuen Fenster.

    Args:
        username (str): Der Benutzername des Admins.
        user_id (int): Die ID des Admin-Benutzers.

    Fehlerbehandlung:
    ------------------
    - Gibt eine Fehlermeldung aus, falls ein Fehler beim Start der GUI auftritt.
    """
    try:
        root = ctk.CTk()
        admin_gui = AdminGUI(root, username, user_id)
        root.mainloop()
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
    