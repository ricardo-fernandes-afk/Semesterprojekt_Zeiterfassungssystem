"""
Modul: Kalender-Frame für TimeArch.

Dieses Modul stellt ein grafisches Kalender-Widget bereit, das die Auswahl von Daten ermöglicht. Es aktualisiert die angezeigten Daten und Diagramme basierend auf der Auswahl im Kalender.

Klassen:
--------
- CalendarFrame: Hauptklasse für die Verwaltung des Kalender-Widgets.

Methoden:
---------
- __init__(self, master, time_entry_frame=None, diagram_frame=None): Initialisiert das Kalender-Frame und verbindet es mit dem Zeitbuchungs- und Diagramm-Frame.
- create_widgets(self): Erstellt das Kalender-Widget und bindet Ereignisse.
- load_for_today(self): Lädt die Daten für das aktuelle Datum und aktualisiert verbundene Frames.
- on_date_selected(self, event=None): Verarbeitet die Auswahl eines Datums und aktualisiert die verbundene Benutzeroberfläche.

Verwendung:
-----------
    from gui_calendar_frame import CalendarFrame

    frame = CalendarFrame(master, time_entry_frame=entry_frame, diagram_frame=diag_frame)
    frame.pack()
"""

import customtkinter as ctk
from tkcalendar import Calendar
from gui.gui_appearance_color import appearance_color, get_default_styles

class CalendarFrame(ctk.CTkFrame):
    """
    Eine Klasse, die ein Kalender-Widget bereitstellt und Interaktionen mit anderen GUI-Komponenten ermöglicht.

    Diese Klasse ermöglicht:
    - Die Auswahl eines Datums.
    - Die Aktualisierung von Zeitbuchungen und Diagrammen basierend auf der Datumswahl.
    """
    def __init__(self, master,time_entry_frame=None, diagram_frame=None):
        """
        Initialisiert den Kalender-Frame.

        Args:
            master (ctk.CTk): Das übergeordnete Fenster.
            time_entry_frame (Frame, optional): Der Frame für Zeitbuchungen, der aktualisiert werden soll. Standard ist None.
            diagram_frame (Frame, optional): Der Frame für Diagramme, der aktualisiert werden soll. Standard ist None.
        """
        self.colors = appearance_color()
        self.styles = get_default_styles
             
        super().__init__(master, corner_radius=10, fg_color=self.colors["alt_background"])
        self.diagram_frame = diagram_frame
        self.time_entry_frame = time_entry_frame
        self.create_widgets()

    def create_widgets(self):
        """
        Erstellt das Kalender-Widget und bindet Ereignisse.

        - Setzt das Design und die Farben basierend auf den GUI-Einstellungen.
        - Bindet das Ereignis `<<CalendarSelected>>`, um die Benutzerinteraktion zu verarbeiten.
        """
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
        """
        Lädt die Daten für das aktuelle Datum und aktualisiert verbundene Frames.

        - Ruft das aktuelle Datum ab.
        - Aktualisiert den Zeitbuchungs-Frame und das Diagramm-Frame, falls vorhanden.
        """
        today = self.calendar.get_date()
        if self.master.time_entry_frame:
            self.master.time_entry_frame.update_date(today)
        if hasattr(self.master.diagram_frame, "user_hours_diagram"):
            self.master.diagram_frame.user_hours_diagram.refresh_diagram(today)
        
    def on_date_selected(self, event=None):
        """
        Verarbeitet die Auswahl eines Datums.

        Args:
            event (Event, optional): Das Ereignis, das durch die Auswahl ausgelöst wurde. Standard ist None.

        - Ruft das ausgewählte Datum ab.
        - Aktualisiert den Zeitbuchungs-Frame und das Diagramm-Frame basierend auf der Auswahl.
        """
        selected_date = self.calendar.get_date()
        if self.master.time_entry_frame:
            self.master.time_entry_frame.update_date(selected_date)
        if hasattr(self.master.diagram_frame, "user_hours_diagram"):
            self.master.diagram_frame.user_hours_diagram.refresh_diagram(selected_date)
