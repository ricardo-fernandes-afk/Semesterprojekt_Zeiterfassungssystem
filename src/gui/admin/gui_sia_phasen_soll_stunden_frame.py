"""
Modul: SIA-Phasen-Soll-Stunden-Frame für TimeArch.

Dieses Modul stellt die grafische Benutzeroberfläche zur Verwaltung der Soll-Stunden für die einzelnen SIA-Phasen eines Projekts bereit.
Es ermöglicht das Laden, Bearbeiten und Speichern der Soll-Stunden direkt in der Benutzeroberfläche.

Klassen:
--------
- SIAPhasenSollStundenFrame: Stellt die GUI zur Verwaltung der Soll-Stunden pro SIA-Phase bereit.

Methoden:
---------
- __init__(self, master, project_number): Initialisiert den Frame mit dem Projektkontext.
- create_widgets(self): Erstellt die Widgets zur Anzeige und Bearbeitung der Soll-Stunden.
- save_soll_stunden(self): Speichert die Soll-Stunden in der Datenbank.
- load_soll_stunden(self): Lädt die Soll-Stunden aus der Datenbank und zeigt sie in den Eingabefeldern an.
- edit_soll_stunden(self): Aktiviert die Bearbeitung der Soll-Stunden.
- toggle_entries(self, state="normal"): Aktiviert oder deaktiviert die Eingabefelder basierend auf dem angegebenen Zustand.

Verwendung:
-----------
    from gui_sia_phasen_soll_stunden_frame import SIAPhasenSollStundenFrame

    frame = SIAPhasenSollStundenFrame(master, project_number="P123")
    frame.pack()
"""

import customtkinter as ctk
from features.features_load_sia_phases import load_sia_phases
from features.feature_save_soll_stunden import save_soll_stunden
from features.feature_load_soll_stunden import load_soll_stunden
from gui.gui_appearance_color import appearance_color, get_default_styles

class SIAPhasenSollStundenFrame(ctk.CTkFrame):
    """
    Eine Klasse, die eine grafische Oberfläche zur Verwaltung der Soll-Stunden für SIA-Phasen bereitstellt.

    Ermöglicht das Laden, Bearbeiten und Speichern von Soll-Stunden für ein bestimmtes Projekt.
    """
    def __init__(self, master, project_number):
        """
        Initialisiert den Frame mit Projektkontext.

        Args:
            master (ctk.CTk): Das übergeordnete Fenster.
            project_number (str): Die Projektnummer, für die die Soll-Stunden angezeigt und bearbeitet werden sollen.
        """
        self.colors = appearance_color()
        self.styles = get_default_styles()
        
        super().__init__(master, corner_radius=10, fg_color=self.colors["alt_background"])
        self.project_number = project_number
        self.soll_stunden_entries = {}
        self.create_widgets()
        self.is_editable = False
        self.load_soll_stunden()

    def create_widgets(self):
        """
        Erstellt die Widgets zur Anzeige und Bearbeitung der Soll-Stunden.

        - Fügt Labels und Eingabefelder für jede SIA-Phase hinzu.
        - Erstellt Buttons für das Speichern und Bearbeiten der Soll-Stunden.
        """
        sia_phases = load_sia_phases()
        
        self.title = ctk.CTkLabel(self, text="Soll Stunden pro SIA-Phase", **self.styles["subtitle"])
        self.title.pack(padx=10, pady=(10,0))
        
        sia_phase_frame = ctk.CTkFrame(self, fg_color=self.colors["alt_background"])
        sia_phase_frame.pack(padx=10, fill="x")

        # SIA-Phasen nebeneinander anordnen
        for col, phase in enumerate(sia_phases):
            phase_label = ctk.CTkLabel(sia_phase_frame, text=phase, **self.styles["text"])
            phase_label.grid(row=0, column=col, sticky="nsew")

            entry = ctk.CTkEntry(sia_phase_frame, placeholder_text="Soll-Stunden", **self.styles["entry"])
            entry.grid(row=1, column=col, padx=10, sticky="nsew")
            self.soll_stunden_entries[phase] = entry

        # Spalten gleichmäßig verteilen
        for col in range(0,4):
            sia_phase_frame.grid_columnconfigure(col, weight=1)

        # Speichern-Button in der dritten Zeile
        self.save_button = ctk.CTkButton(
            sia_phase_frame,
            text="Speichern",
            command=self.save_soll_stunden,
            **self.styles["button"],
        )
        self.save_button.grid(row=2, column=1, padx=10, pady=10, sticky="e")
        
        # Bearbeiten-Button in der dritten Zeile
        self.edit_button = ctk.CTkButton(
            sia_phase_frame,
            text="Bearbeiten",
            command=self.edit_soll_stunden,
            **self.styles["button_secondary"],
        )
        self.edit_button.grid(row=2, column=2, padx=10, pady=10, sticky="w")

    def save_soll_stunden(self):
        """
        Speichert die Soll-Stunden in der Datenbank.

        - Verwendet die Funktion `save_soll_stunden`, um die Eingabewerte in der Datenbank zu speichern.
        - Deaktiviert die Eingabefelder nach dem Speichern.
        """
        save_soll_stunden(self)
        self.toggle_entries(state="disabled")
        self.is_editable = False

    def load_soll_stunden(self):
        """
        Lädt die Soll-Stunden aus der Datenbank und zeigt sie in den Eingabefeldern an.

        - Verwendet die Funktion `load_soll_stunden`, um die Soll-Stunden aus der Datenbank abzurufen.
        - Deaktiviert die Eingabefelder nach dem Laden.
        """
        load_soll_stunden(self)
        self.toggle_entries(state="disabled")
        
    def edit_soll_stunden(self):
        """
        Aktiviert die Bearbeitung der Soll-Stunden.

        - Schaltet die Eingabefelder in den Bearbeitungsmodus.
        """
        self.toggle_entries(state="normal")
        self.is_editable = True
    
    def toggle_entries(self, state="normal"):
        """
        Aktiviert oder deaktiviert die Eingabefelder basierend auf dem angegebenen Zustand.

        Args:
            state (str): Der Zustand der Eingabefelder. Standard ist "normal".
        """
        for entry in self.soll_stunden_entries.values():
            entry.configure(state=state)

