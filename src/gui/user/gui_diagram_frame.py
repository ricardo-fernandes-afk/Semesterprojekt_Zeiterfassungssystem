import customtkinter as ctk
from features.feature_diagram_user_hours import UserHoursDiagram
from gui.gui_appearance_color import appearance_color

class DiagramFrame(ctk.CTkFrame):
    def __init__(self, master, user_id):
        self.colors = appearance_color()
        super().__init__(master, fg_color=self.colors["alt_background"])
        self.user_id = user_id
        self.create_widgets()
    
    def create_widgets(self):
        # Benutzer-Diagramm rechts
        self.user_hours_diagram = UserHoursDiagram(self, self.user_id)
        self.user_hours_diagram.grid(row=0, column=1, padx=10, sticky="nsew")

        # Projektphasen-Diagramm links
        

        # Grid-Konfiguration
        self.grid_columnconfigure(0, weight=5)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
