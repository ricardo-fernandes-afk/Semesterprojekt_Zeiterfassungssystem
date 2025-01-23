"""
Modul: Benutzer-Auswahl-Frame für TimeArch.

Dieses Modul stellt eine grafische Benutzeroberfläche bereit, die dem Benutzer die Auswahl eines Projekts oder einer Aufgabe ermöglicht. Es integriert verschiedene Frames, um SIA-Phasen, Kalender, Zeitbuchungen und Diagramme anzuzeigen.

Klassen:
--------
- UserSelectedFrame: Hauptklasse zur Anzeige und Verwaltung der Benutzer-Auswahlansicht.

Methoden:
---------
- __init__(self, master, user_id, username, selected_id=None, selected_name=None, description=None): Initialisiert den Frame mit Benutzer- und Projektdetails.
- clear_widgets(self): Entfernt alle Widgets aus dem Frame.
- create_widgets(self): Erstellt die grundlegenden Widgets wie Titel und Beschreibung.
- create_title_label(self): Erstellt und gibt das Titel-Label für den Frame zurück.
- create_description_label(self): Erstellt und gibt das Beschreibungs-Label für den Frame zurück.
- update_project_details(self, selected_id, selected_name, description=None): Aktualisiert die Widgets und Frames basierend auf der Auswahl eines neuen Projekts.

Verwendung:
-----------
    from gui_user_selected_frame import UserSelectedFrame

    frame = UserSelectedFrame(master, user_id=1, username="John Doe", selected_id="P123", selected_name="Projekt A")
    frame.pack()
"""

import customtkinter as ctk
from gui.user.gui_choose_sia_phase_frame import ChooseSIAPhaseFrame
from gui.user.gui_calendar_frame import CalendarFrame
from gui.user.gui_time_entry_frame import TimeEntryFrame
from gui.user.gui_diagram_frame import DiagramFrame
from gui.user.gui_intern_infos import InternInfosFrame
from gui.gui_appearance_color import appearance_color, get_default_styles

class UserSelectedFrame(ctk.CTkFrame):
    """
    Eine Klasse zur Verwaltung der Benutzer-Auswahlansicht.

    Funktionen:
    - Anzeige von Projektdetails
    - Integration von SIA-Phasen, Kalender, Zeitbuchungen und Diagrammen
    """
    def __init__(self, master, user_id, username, selected_id=None, selected_name=None, description=None):
        """
        Initialisiert den Frame mit Benutzer- und Projektdetails.

        Args:
            master (ctk.CTk): Das übergeordnete Fenster.
            user_id (int): Die ID des aktuellen Benutzers.
            username (str): Der Benutzername.
            selected_id (str, optional): Die ID des ausgewählten Projekts. Standard ist None.
            selected_name (str, optional): Der Name des ausgewählten Projekts. Standard ist None.
            description (str, optional): Eine Beschreibung des ausgewählten Projekts. Standard ist None.
        """
        self.colors = appearance_color()
        self.styles = get_default_styles()
        
        super().__init__(master, corner_radius=10, fg_color=self.colors["background"])
        self.grid_propagate(False)
        self.user_id = user_id
        self.username = username
        self.selected_id = selected_id
        self.selected_name = selected_name
        self.description = description
        self.time_entry_frame = None
        self.selected_project_number = None
        self.diagram_frame = None
        self.create_widgets()
        
        self.grid_rowconfigure(0, minsize=100, weight=1)
        self.grid_rowconfigure(1, minsize=50, weight=1)
        self.grid_rowconfigure(2, minsize=250, weight=1)
        self.grid_rowconfigure(3, minsize=450, weight=2)
        self.grid_rowconfigure(4, minsize=250, weight=2)
        for col in range(2):
            self.grid_columnconfigure(col, weight=1)
    
    def clear_widgets(self):
        """
        Entfernt alle Widgets aus dem Frame.

        - Löscht alle untergeordneten Widgets.
        - Setzt alle Frame-Attribute auf None.
        """
        for widget in self.winfo_children():
            widget.destroy()
        self.time_entry_frame = None
        self.choose_sia_phase_frame = None
        self.calendar_frame = None
        self.diagram_frame = None
        self.inter_infos_frame = None

    def create_widgets(self):
        """
        Erstellt die grundlegenden Widgets wie Titel und Beschreibung.

        - Fügt das Titel-Label und das Beschreibungs-Label hinzu.
        """
        self.title_label = self.create_title_label()
        self.description_label = self.create_description_label()

    def create_title_label(self):
        """
        Erstellt und gibt das Titel-Label für den Frame zurück.

        Returns:
            ctk.CTkLabel: Das erstellte Titel-Label.
        """
        title_text = f"{self.selected_id} {self.selected_name}" if self.selected_name else "Wählen Sie ein Projekt"
        title_label = ctk.CTkLabel(self, text=title_text, **self.styles["title"])
        title_label.grid(row=0, columnspan=2, pady=10, sticky="nsew")
        return title_label

    def create_description_label(self):
        """
        Erstellt und gibt das Beschreibungs-Label für den Frame zurück.

        Returns:
            ctk.CTkLabel: Das erstellte Beschreibungs-Label.
        """
        description_label = ctk.CTkLabel(self, text="", **self.styles["description"], wraplength=500)
        description_label.grid(row=1, columnspan=2, sticky="nsew")
        return description_label

    def update_project_details(self, selected_id, selected_name, description=None):
        """
        Aktualisiert die Widgets und Frames basierend auf der Auswahl eines neuen Projekts.

        Args:
            selected_id (str): Die ID des ausgewählten Projekts.
            selected_name (str): Der Name des ausgewählten Projekts.
            description (str, optional): Eine Beschreibung des ausgewählten Projekts. Standard ist None.

        - Aktualisiert die Titel- und Beschreibungs-Labels.
        - Integriert die relevanten Frames wie SIA-Phasen, Kalender, Zeitbuchungen und Diagramme.
        """
        self.clear_widgets()
        self.create_widgets()       
        self.selected_id = selected_id
        self.selected_name = selected_name
        self.description = description
        self.selected_project_number = selected_id
        
        self.title_label.configure(text=f"{selected_id} - {selected_name}")
        self.description_label.configure(text=self.description) 
        
        if selected_id != "0000":
            self.choose_sia_phase_frame = ChooseSIAPhaseFrame(self, project_number=self.selected_id)
            self.choose_sia_phase_frame.grid(row=2, columnspan=2, padx=10, pady=10, sticky="nsew")
        else:
            self.inter_infos_frame = InternInfosFrame(self, self.user_id, self.username)
            self.inter_infos_frame.grid(row=2, columnspan=2, padx=10, pady=10, sticky="nsew")
                
        self.calendar_frame = CalendarFrame(self, time_entry_frame=None, diagram_frame=None)
        self.calendar_frame.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
        
        self.time_entry_frame = TimeEntryFrame(self)
        self.time_entry_frame.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")
        
        self.diagram_frame = DiagramFrame(self, self.user_id, project_number=self.selected_id)
        self.diagram_frame.grid(row=4, columnspan=2, padx=10, pady=10, sticky="nsew")
        
        self.calendar_frame.load_for_today()

