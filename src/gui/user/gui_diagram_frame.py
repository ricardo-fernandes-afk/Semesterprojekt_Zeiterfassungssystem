import customtkinter as ctk
from features.feature_diagram_user_hours import UserHoursDiagram
from features.feature_diagram_project_phase import ProjectPhaseDiagram
from gui.gui_appearance_color import appearance_color

class DiagramFrame(ctk.CTkFrame):
    def __init__(self, master, user_id, project_number):
        self.colors = appearance_color()
        super().__init__(master,corner_radius=10, fg_color=self.colors["background_light"])
        self.user_id = user_id
        self.project_number = project_number
        self.create_widgets()
    
    def create_widgets(self):
        # Benutzer-Diagramm rechts
        self.user_hours_diagram = UserHoursDiagram(self, self.user_id)
        self.user_hours_diagram.grid(row=0, column=1, sticky="nsew")

        # Projektphasen-Diagramm links
        if self.project_number != "0000":
            self.project_phase_diagram = ProjectPhaseDiagram(self, self.user_id, self.project_number)
            self.project_phase_diagram.grid(row=0, column=0, sticky="nsew")
        else:
            self.project_phase_diagram = ctk.CTkFrame(self, corner_radius=10, fg_color=self.colors["alt_background"])
            self.project_phase_diagram.grid(row=0, column=0, sticky="nsew")
            self.project_phase_diagram.configure(height=0)

        # Grid-Konfiguration
        self.grid_columnconfigure(0, weight=6, minsize=800)
        self.grid_columnconfigure(1, weight=1, minsize=300)
        self.grid_rowconfigure(0, weight=1)
