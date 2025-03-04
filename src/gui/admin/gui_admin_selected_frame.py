"""
Modul: SelectedFrame für TimeArch.

Dieses Modul stellt die grafische Benutzeroberfläche für die Anzeige und Bearbeitung von Projekten oder Benutzerdetails bereit.
Es unterstützt die Anzeige von Projektphasen, zugehörigen Benutzern und Diagrammen sowie die Verwaltung von Benutzergrundinformationen.

Klassen:
--------
- SelectedFrame: Hauptklasse zur Darstellung und Verwaltung von Projekten und Benutzern.

Methoden:
---------
- __init__(self, master, user_id=None, selected_id=None, selected_name=None, description=None): Initialisiert das SelectedFrame mit den übergebenen Parametern.
- clear_widgets(self): Entfernt alle Widgets im Frame.
- create_widgets(self): Erstellt die Standard-Widgets (Titel und Beschreibung).
- create_title_label(self): Erstellt das Titel-Label für das SelectedFrame.
- create_description_label(self): Erstellt das Beschreibungs-Label für das SelectedFrame.
- update_project_details(self, selected_id, selected_name, description=None): Aktualisiert die Details und Widgets für ein ausgewähltes Projekt.
- update_user_details(self, selected_user_id, selected_username): Aktualisiert die Details und Widgets für einen ausgewählten Benutzer.

Verwendung:
-----------
    from gui_admin_selected_frame import SelectedFrame

    selected_frame = SelectedFrame(master, user_id, selected_id, selected_name, description)
    selected_frame.update_project_details("P123", "Projektname", "Projektbeschreibung")
"""

import customtkinter as ctk
from gui.admin.gui_sia_phasen_soll_stunden_frame import SIAPhasenSollStundenFrame
from gui.admin.gui_user_to_project_frame import UserToProjectFrame
from gui.admin.gui_stunden_uebersicht_project import StundenUebersichtProjectFrame
from gui.admin.gui_grundinfos_user import GrundInfosUser
from gui.admin.gui_stunden_uebersicht_user import StundenUebersichtUserFrame
from features.feature_diagram_admin_project import AdminProjectDiagram
from features.feature_diagram_vacation import VacationDiagram
from features.feature_diagram_employment_percentage import EmploymentPercentageDiagram
from features.feature_diagram_total_hours import DiagramTotalHours
from gui.gui_appearance_color import appearance_color, get_default_styles

class SelectedFrame(ctk.CTkFrame):
    """
    Eine Klasse zur Darstellung und Verwaltung der Details für Projekte und Benutzer.

    Diese Klasse unterstützt die Anzeige von Projektphasen, zugehörigen Benutzern, Diagrammen und Benutzerinformationen.
    """
    def __init__(self, master, user_id=None, selected_id=None, selected_name=None, description=None):
        """
        Initialisiert das SelectedFrame.

        Args:
            master (ctk.CTk): Das übergeordnete Fenster.
            user_id (int, optional): Die Benutzer-ID, wenn ein Benutzer ausgewählt ist.
            selected_id (str, optional): Die Projektnummer oder Benutzer-ID des ausgewählten Eintrags.
            selected_name (str, optional): Der Name des ausgewählten Projekts oder Benutzers.
            description (str, optional): Die Beschreibung des ausgewählten Projekts.
        """
        self.colors = appearance_color()
        self.styles = get_default_styles()
        
        super().__init__(master, corner_radius=10, fg_color=self.colors["background"])
        self.grid_propagate(False)
        self.user_id = user_id
        self.selected_id = selected_id
        self.selected_name = selected_name
        self.description = description
        self.soll_stunden_entries = {}
        self.sia_phases_frame = None
        self.user_to_project_frame = None
        
        self.create_widgets()
        
        self.grid_rowconfigure(0, minsize=100, weight=1)
        self.grid_rowconfigure(1, minsize=50, weight=1)
        self.grid_rowconfigure(2, minsize=250, weight=1)
        self.grid_rowconfigure(3, minsize=450, weight=2)
        self.grid_rowconfigure(4, minsize=250, weight=2)
        for col in range(0,4):
            self.grid_columnconfigure(col, weight=1)
            

    def clear_widgets(self):
        """
        Entfernt alle Widgets aus dem Frame.
        """
        for widget in self.winfo_children():
            widget.destroy()

    def create_widgets(self):
        """
        Erstellt die Standard-Widgets (Titel und Beschreibung) für das SelectedFrame.
        """
        self.title_label = self.create_title_label()
        self.description_label = self.create_description_label()

    def create_title_label(self):
        """
        Erstellt das Titel-Label für das SelectedFrame.

        Returns:
            ctk.CTkLabel: Das erstellte Titel-Label.
        """
        title_text = f"{self.selected_id} {self.selected_name}" if self.selected_name else "Wählen Sie ein Projekt oder einen Benutzer"
        title_label = ctk.CTkLabel(self, text=title_text, **self.styles["title"])
        title_label.grid(row=0, columnspan=4, pady=5, sticky="nsew")
        return title_label

    def create_description_label(self):
        """
        Erstellt das Beschreibungs-Label für das SelectedFrame.

        Returns:
            ctk.CTkLabel: Das erstellte Beschreibungs-Label.
        """
        description_label = ctk.CTkLabel(self, text="", **self.styles["description"], wraplength=500)
        description_label.grid(row=1, columnspan=4, sticky="nsew")
        return description_label

    def update_project_details(self, selected_id, selected_name, description=None):
        """
        Aktualisiert die Details und Widgets für ein ausgewähltes Projekt.

        Args:
            selected_id (str): Die Projektnummer des ausgewählten Projekts.
            selected_name (str): Der Name des ausgewählten Projekts.
            description (str, optional): Die Beschreibung des ausgewählten Projekts.
        """
        self.clear_widgets()
        self.create_widgets()
        
        self.selected_id = selected_id
        self.selected_name = selected_name
        self.description = description        

        self.title_label.configure(text=f"{selected_id} - {selected_name}")
        self.description_label.configure(text=self.description if self.description else "")

        if selected_id != "0000":
            self.sia_phases_frame = SIAPhasenSollStundenFrame(self, project_number=selected_id)
            self.sia_phases_frame.grid(row=2, columnspan=4, padx=10, pady=10, sticky="nsew")
        else:
            self.sia_phases_frame = ctk.CTkFrame(self, fg_color=self.colors["alt_background"])
            self.sia_phases_frame.grid(row=2, columnspan=4, padx=10, pady=10, sticky="nsew")
        
        self.user_to_project_frame = UserToProjectFrame(self, project_number=selected_id)
        self.user_to_project_frame.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
        
        self.stunden_uebersicht_project_frame = StundenUebersichtProjectFrame(self, project_number=selected_id)
        self.stunden_uebersicht_project_frame.grid(row=3, column=1, columnspan=3, padx=10, pady=10, sticky="nsew")
        
        if selected_id != "0000":
            self.diagram_frame = AdminProjectDiagram(self, project_number=selected_id, filter_frame=self.stunden_uebersicht_project_frame)
            self.diagram_frame.grid(row=4, columnspan=4, padx=10, pady=10, sticky="nsew")
        else:
            self.diagram_frame = ctk.CTkFrame(self, fg_color=self.colors["alt_background"])

    def update_user_details(self, selected_user_id, selected_username):
        """
        Aktualisiert die Details und Widgets für einen ausgewählten Benutzer.

        Args:
            selected_user_id (int): Die Benutzer-ID des ausgewählten Benutzers.
            selected_username (str): Der Name des ausgewählten Benutzers.
        """
        self.clear_widgets()
        self.create_widgets()

        self.selected_id = selected_user_id
        self.selected_name = selected_username

        self.title_label.configure(text=f"{selected_username}")
        self.description_label.configure(text="")

        self.grundinfos_user_frame = GrundInfosUser(self, user_id=selected_user_id)
        self.grundinfos_user_frame.grid(row=2, columnspan=4, padx=10, pady=10, sticky="nsew")

        self.stunden_uebersicht_user_frame = StundenUebersichtUserFrame(self, user_id=selected_user_id)
        self.stunden_uebersicht_user_frame.grid(row=3, columnspan=4, padx=10, pady=10, sticky="nsew")

        self.diagram_frame = ctk.CTkFrame(self, fg_color=self.colors["background"])
        self.diagram_frame.grid(row=4, columnspan=4, padx=10, pady=10, sticky="nsew")
        
        self.vacation_diagram = VacationDiagram(self.diagram_frame, user_id=selected_user_id)
        self.vacation_diagram.grid(row=0, column=0, sticky="nsew")
        
        self.employment_percentage_diagram = EmploymentPercentageDiagram(self.diagram_frame, user_id=selected_user_id)
        self.employment_percentage_diagram.grid(row=0, column=1, sticky="nsew")
        
        self.total_hours_diagram = DiagramTotalHours(self.diagram_frame, user_id=selected_user_id)
        self.total_hours_diagram.grid(row=0, column=2, sticky="nsew")
        
        self.diagram_frame.grid_rowconfigure(0, weight=1)
        for col in range(3):
            self.diagram_frame.grid_columnconfigure(col, weight=1)
        
            
            
