import customtkinter as ctk

class GrundinfosUser(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=10)
        
        # Label für Grundinformationen
        self.title_label = ctk.CTkLabel(self, text="Grundinformationen Angestellter", font=("", 16, "bold"))
        self.title_label.pack(pady=10, padx=10)
        
        # Hier könnten später spezifische Felder wie Arbeitsprozentsatz, Urlaubstage usw. hinzugefügt werden
