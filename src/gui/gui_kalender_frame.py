import customtkinter as ctk
from tkcalendar import Calendar
from datetime import date

class KalenderFrame(ctk.CTkFrame):
    def __init__(self, master, stunden_uebersicht_frame):
        super().__init__(master, corner_radius=10)
        self.stunden_uebersicht_frame = stunden_uebersicht_frame
        self.create_widgets()

    def create_widgets(self):
        # Kalender Widget
        self.calendar = Calendar(self, selectmode="day", year=date.today().year, month=date.today().month)
        self.calendar.pack(padx=10, pady=10)
        
        # Button zum Aktualisieren der Stundenübersicht
        update_button = ctk.CTkButton(self, text="Stunden anzeigen", command=self.update_stunden_uebersicht)
        update_button.pack(pady=10)

    def update_stunden_uebersicht(self):
        selected_date = self.calendar.get_date()
        year, month, _ = map(int, selected_date.split("-"))
        self.stunden_uebersicht_frame.update_stunden(year, month)
