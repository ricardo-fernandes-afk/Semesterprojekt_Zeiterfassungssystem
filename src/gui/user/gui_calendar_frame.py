import customtkinter as ctk
from tkcalendar import Calendar

class CalendarFrame(ctk.CTkFrame):
    def __init__(self, master, stunden_uebersicht_frame=None):
        super().__init__(master, corner_radius=10)
        self.stunden_uebersicht_frame = stunden_uebersicht_frame
        self.create_widgets()

    def create_widgets(self):
        # Kalender Widget
        self.calendar = Calendar(self, selectmode="day", date_pattern="yyyy-mm-dd", font=("", 14))
        self.calendar.pack(padx=10, pady=10, fill="both", expand=True)
        
        self.calendar.bind("<<CalendarSelected>>", self.on_date_selected)
        
    def on_date_selected(self, event=None):
        selected_date = self.calendar.get_date()
        if self.stunden_uebersicht_frame:
            self.stunden_uebersicht_frame.update_date(selected_date)
