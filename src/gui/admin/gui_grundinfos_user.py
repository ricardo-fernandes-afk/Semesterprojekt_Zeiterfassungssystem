import customtkinter as ctk
from gui.gui_appearance_color import appearance_color, get_default_styles

class GrundinfosUser(ctk.CTkFrame):
    def __init__(self, master):
        self.colors = appearance_color()
        self.styles = get_default_styles()
        super().__init__(master, corner_radius=10)
        
        # Label für Grundinformationen
        self.title_label = ctk.CTkLabel(self, text="Grundinformationen Angestellter", **self.styles["subtitle"])
        self.title_label.pack(pady=10, padx=10)
        
        # Hier könnten später spezifische Felder wie Arbeitsprozentsatz, Urlaubstage usw. hinzugefügt werden
