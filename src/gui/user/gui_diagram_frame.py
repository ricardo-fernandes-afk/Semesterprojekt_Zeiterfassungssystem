"""
Modul: Diagram-Frame für TimeArch.

Dieses Modul erstellt ein Frame, das mehrere Diagramme für Benutzer und Projekte anzeigt. Es integriert Diagramme
wie Benutzerstunden, Projektphasen, Urlaubstage und Gesamtstunden, abhängig von den Eingabewerten.

Klassen:
--------
- DiagramFrame: Stellt das Diagram-Frame bereit und verwaltet die Anzeige mehrerer Diagrammtypen.

Methoden:
---------
- __init__(self, master, user_id, project_number): Initialisiert das Diagram-Frame mit Benutzer- und Projektkontext.
- create_widgets(self): Erstellt und platziert die Diagramm-Widgets basierend auf den übergebenen Parametern.

Verwendung:
-----------
    from gui_diagram_frame import DiagramFrame

    frame = DiagramFrame(master, user_id=1, project_number="P123")
    frame.pack()
"""

import customtkinter as ctk
from features.feature_diagram_user_hours import UserHoursDiagram
from features.feature_diagram_project_phase import ProjectPhaseDiagram
from features.feature_diagram_vacation import VacationDiagram
from features.feature_diagram_total_hours import DiagramTotalHours
from gui.gui_appearance_color import appearance_color

class DiagramFrame(ctk.CTkFrame):
    """
    Eine Klasse, die ein Diagramm-Frame bereitstellt.

    Dieses Frame visualisiert unterschiedliche Diagramme basierend auf dem Benutzer- und Projektkontext:
    - Benutzerstunden
    - Projektphasen
    - Urlaubstage
    - Gesamtstunden
    """
    def __init__(self, master, user_id, project_number):
        """
        Initialisiert das Diagram-Frame mit Benutzer- und Projektkontext.

        Args:
            master (ctk.CTk): Das übergeordnete Fenster.
            user_id (int): Die ID des Benutzers, dessen Daten angezeigt werden sollen.
            project_number (str): Die Projektnummer, deren Daten angezeigt werden sollen.
        """
        self.colors = appearance_color()
        super().__init__(master,corner_radius=10, fg_color=self.colors["background"])
        self.user_id = user_id
        self.project_number = project_number
        self.create_widgets()
    
    def create_widgets(self):
        """
        Erstellt und platziert die Diagramm-Widgets basierend auf den übergebenen Parametern.

        - Zeigt das Benutzerstunden-Diagramm auf der rechten Seite an.
        - Zeigt entweder das Projektphasen-Diagramm oder die Urlaubstage- und Gesamtstunden-Diagramme
          basierend auf der Projektnummer an.
        - Konfiguriert das Grid für eine gleichmäßige Darstellung der Diagramme.
        """
        # Benutzer-Diagramm rechts
        self.user_hours_diagram = UserHoursDiagram(self, self.user_id)
        self.user_hours_diagram.grid(row=0, column=2, sticky="nsew")

        # Projektphasen-Diagramm links
        if self.project_number != "0000":
            self.project_phase_diagram = ProjectPhaseDiagram(self, self.user_id, self.project_number)
            self.project_phase_diagram.grid(row=0, column=0, columnspan=2, sticky="nsew")
        else:
            self.vacation_diagram = VacationDiagram(self, self.user_id)
            self.vacation_diagram.grid(row=0, column=0, sticky="nsew")
            
            self.total_hours_diagram = DiagramTotalHours(self, self.user_id)
            self.total_hours_diagram.grid(row=0, column=1, sticky="nsew")      

        # Grid-Konfiguration
        for col in range(3):
            self.grid_columnconfigure(col, weight=1, minsize=300)
        self.grid_rowconfigure(0, weight=1)
