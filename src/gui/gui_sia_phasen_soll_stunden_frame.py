import customtkinter as ctk
from features.features_load_sia_phases import load_sia_phases
from features.feature_save_soll_stunden import save_soll_stunden
from features.feature_load_soll_stunden import load_soll_stunden

class SIAPhasenSollStundenFrame(ctk.CTkFrame):
    def __init__(self, master, project_number):
        super().__init__(master)
        self.project_number = project_number
        self.soll_stunden_entries = {}
        self.create_widgets()
        self.is_editable = False

    def create_widgets(self):
        sia_phases = load_sia_phases()
        
        self.title = ctk.CTkLabel(self, text="Soll Stunden pro SIA-Phase", font=("", 16, "bold"))
        self.title.grid(row=0, columnspan=4, pady=5, sticky="nsew")

        # SIA-Phasen nebeneinander anordnen
        for col, phase in enumerate(sia_phases):
            phase_label = ctk.CTkLabel(self, text=phase, font=("", 14))
            phase_label.grid(row=1, column=col, pady=(5,0), sticky="nsew")

            entry = ctk.CTkEntry(self, placeholder_text="Soll-Stunden")
            entry.grid(row=2, column=col, padx=20, sticky="nsew")
            self.soll_stunden_entries[phase] = entry

        # Spalten gleichmäßig verteilen
        for col in range(0,4):
            self.grid_columnconfigure(col, weight=1)

        # Speichern-Button in der dritten Zeile
        self.save_button = ctk.CTkButton(self, text="Soll-Stunden speichern", command=self.save_soll_stunden)
        self.save_button.grid(row=3, columnspan=4, pady=5)
        
        # Bearbeiten-Button in der dritten Zeile
        self.edit_button = ctk.CTkButton(self, text="Soll-Stunden bearbeiten", command=self.edit_soll_stunden, fg_color="#000fff")
        self.edit_button.grid(row=4, columnspan=4, pady=5)

    def save_soll_stunden(self):
        save_soll_stunden(self)
        self.toggle_entries(state="disabled")
        self.is_editable = False

    def load_soll_stunden(self):
        load_soll_stunden(self)
        self.toggle_entries(state="disabled")
        
    def edit_soll_stunden(self):
        self.toggle_entries(state="normal")
        self.is_editable = True
    
    def toggle_entries(self, state="normal"):
        for entry in self.soll_stunden_entries.values():
            entry.configure(state=state)

