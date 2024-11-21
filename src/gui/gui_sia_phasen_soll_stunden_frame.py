import customtkinter as ctk
from features.features_load_sia_phases import load_sia_phases
from features.feature_save_soll_stunden import save_soll_stunden
from features.feature_load_soll_stunden import load_soll_stunden

class SIAPhasenSollStundenFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.soll_stunden_entries = {}
        self.create_widgets()

    def create_widgets(self):
        sia_phases = load_sia_phases()

        # SIA-Phasen nebeneinander anordnen
        for col, phase in enumerate(sia_phases):
            phase_label = ctk.CTkLabel(self, text=phase, font=("", 14))
            phase_label.grid(row=0, column=col, padx=10, pady=5, sticky="nsew")

            entry = ctk.CTkEntry(self, placeholder_text="Soll-Stunden")
            entry.grid(row=1, column=col, padx=50, pady=5, sticky="nsew")
            self.soll_stunden_entries[phase] = entry

        # Spalten gleichmäßig verteilen
        for col in range(len(sia_phases)):
            self.grid_columnconfigure(col, weight=1)

        # Speichern-Button in der dritten Zeile zentriert hinzufügen
        self.save_button = ctk.CTkButton(self, text="Soll-Stunden speichern", command=self.save_soll_stunden)
        self.save_button.grid(row=2, columnspan=len(sia_phases), pady=5)

    def save_soll_stunden(self):
        save_soll_stunden(self)

    def load_soll_stunden(self):
        load_soll_stunden(self)
