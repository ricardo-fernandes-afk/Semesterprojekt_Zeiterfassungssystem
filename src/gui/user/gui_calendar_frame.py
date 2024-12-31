import customtkinter as ctk
from tkcalendar import Calendar
from gui.gui_appearance_color import appearance_color, get_default_styles

class CalendarFrame(ctk.CTkFrame):
    def __init__(self, master,time_entry_frame=None, diagram_frame=None):
        self.colors = appearance_color()
        self.styles = get_default_styles
             
        super().__init__(master, corner_radius=10, fg_color=self.colors["alt_background"])
        self.diagram_frame = diagram_frame
        self.time_entry_frame = time_entry_frame
        self.create_widgets()

    def create_widgets(self):
        # Kalender Widget
        self.calendar = Calendar(
            self, 
            selectmode="day",
            date_pattern="yyyy-mm-dd",
            font="Arial, 14", 
            background=self.colors["background_light"],
            foreground=self.colors["text_dark"],
            headersbackground=self.colors["background_light"],
            headersforeground=self.colors["text_dark"],
            weekendbackground=self.colors["background"],
            weekendforeground=self.colors["text_light"],
            selectbackgroung=self.colors["text_light"],
            selectforeground=self.colors["text_dark"],
        )
        self.calendar.pack(padx=10, pady=10, fill="both", expand=True)
        
        self.calendar.bind("<<CalendarSelected>>", self.on_date_selected)
        
    def load_for_today(self):
        """Lädt die Daten auf das aktuelle Datum."""
        today = self.calendar.get_date()
        if self.master.time_entry_frame:
            self.master.time_entry_frame.update_date(today)
        if hasattr(self.master.diagram_frame, "user_hours_diagram"):
            self.master.diagram_frame.user_hours_diagram.refresh_diagram(today)
        
    def on_date_selected(self, event=None):
        selected_date = self.calendar.get_date()
        if self.master.time_entry_frame:
            self.master.time_entry_frame.update_date(selected_date)
        if hasattr(self.master.diagram_frame, "user_hours_diagram"):
            self.master.diagram_frame.user_hours_diagram.refresh_diagram(selected_date)
