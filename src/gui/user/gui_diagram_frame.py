import customtkinter as ctk
from features.feature_diagram_user_hours import UserHoursDiagram
from features.feature_diagram_project_phase import ProjectPhaseDiagram
from features.feature_diagram_vacation import VacationDiagram
from gui.gui_appearance_color import appearance_color

class DiagramFrame(ctk.CTkFrame):
    def __init__(self, master, user_id, project_number):
        self.colors = appearance_color()
        super().__init__(master,corner_radius=10, fg_color=self.colors["background"])
        self.user_id = user_id
        self.project_number = project_number
        self.create_widgets()
    
    def create_widgets(self):
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
            

        # Grid-Konfiguration
        for col in range(3):
            self.grid_columnconfigure(col, weight=1, minsize=300)
        self.grid_rowconfigure(0, weight=1)
