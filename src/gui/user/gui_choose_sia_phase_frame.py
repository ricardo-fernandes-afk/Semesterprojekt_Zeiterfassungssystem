"""
Modul: SIA-Phasen-Auswahl für TimeArch.

Dieses Modul stellt eine grafische Benutzeroberfläche bereit, um SIA-Phasen für ein Projekt auszuwählen. Es zeigt dynamisch erzeugte Buttons und Labels für die Sollstunden an, die den Phasen zugeordnet sind.

Klassen:
--------
- ChooseSIAPhaseFrame: Hauptklasse zur Auswahl von SIA-Phasen und Anzeige der zugehörigen Sollstunden.

Methoden:
---------
- __init__(self, master, project_number=None): Initialisiert das Frame mit Projektkontext und erstellt Widgets.
- create_widgets(self): Erstellt dynamisch Buttons für SIA-Phasen und Labels für Sollstunden.
- select_phase(self, phase): Markiert die ausgewählte Phase und aktualisiert die Button-Designs.
- get_phase_id(self, phase_name): Ruft die ID einer SIA-Phase basierend auf ihrem Namen aus der Datenbank ab.
- load_soll_stunden(self): Lädt die Sollstunden für jede Phase und zeigt sie in den Labels an.

Verwendung:
-----------
    from gui_choose_sia_phase_frame import ChooseSIAPhaseFrame

    frame = ChooseSIAPhaseFrame(master, project_number="P123")
    frame.pack()
"""

from features.features_load_sia_phases import load_sia_phases
from db.db_connection import create_connection
from gui.gui_appearance_color import appearance_color, get_default_styles
import customtkinter as ctk

class ChooseSIAPhaseFrame(ctk.CTkFrame):
    """
    Eine Klasse, die SIA-Phasen mit dynamischen Buttons und zugehörigen Labels für Sollstunden darstellt.

    Funktionen:
    - Auswahl einer SIA-Phase
    - Laden und Anzeigen der Sollstunden pro Phase
    """
    def __init__(self, master, project_number=None):
        """
        Initialisiert das Frame für die SIA-Phasen-Auswahl.

        Args:
            master (ctk.CTk): Das übergeordnete Fenster.
            project_number (str, optional): Die Projektnummer, um die Sollstunden zu laden. Standard ist None.
        """
        self.colors = appearance_color()
        self.styles = get_default_styles()
        super().__init__(master, corner_radius=10, fg_color=self.colors["alt_background"])
        self.project_number = project_number
        self.selected_phase = None
        self.selected_phase_id = None
        self.buttons = {}  # Speichert Buttons für die SIA-Phasen
        self.soll_stunden_labels = {}  # Speichert Labels für die Sollstunden
        self.create_widgets()
        self.load_soll_stunden()  # Lade Sollstunden beim Initialisieren

    def create_widgets(self):
        """
        Erstellt dynamische Buttons und Labels für die SIA-Phasen.

        - Buttons repräsentieren SIA-Phasen und ermöglichen die Auswahl.
        - Labels zeigen die Sollstunden der jeweiligen Phase an.
        """
        # Titel für den Frame
        title_label = ctk.CTkLabel(self, text="Wähle eine SIA Phase:", **self.styles["subtitle"])
        title_label.pack(padx=10, pady=(10,0))
        
        choose_frame = ctk.CTkFrame(self, fg_color=self.colors["alt_background"])
        choose_frame.pack(padx=10, pady=10, fill="x", expand=True)
        
        for col in range(4):
            choose_frame.grid_columnconfigure(col, weight=1)

        # Dynamische Buttons und Labels für Sollstunden
        phases = load_sia_phases()
        for index, phase in enumerate(phases):
            # Button für die Phase
            button = ctk.CTkButton(
                choose_frame,
                text=phase,
                command=lambda p=phase: self.select_phase(p),
                **self.styles["button"],
            )
            button.grid(row=0, column=index, padx=5, pady=5)
            self.buttons[phase] = button

            # Label für die Sollstunden unter dem Button
            soll_label = ctk.CTkLabel(choose_frame, text="", **self.styles["text"])
            soll_label.grid(row=1, column=index, padx=5, pady=5)
            self.soll_stunden_labels[phase] = soll_label

    def select_phase(self, phase):
        """
        Markiert die ausgewählte Phase und passt die Button-Designs an.

        Args:
            phase (str): Der Name der ausgewählten Phase.
        """
        # Ändere die Farben der Buttons basierend auf der Auswahl
        self.selected_phase = phase
        self.selected_phase_id = self.get_phase_id(phase)
        for btn_phase, button in self.buttons.items():
            button.configure(fg_color=self.colors["disabled"])
        if phase in self.buttons:
            self.buttons[phase].configure(fg_color=self.colors["primary"])
            
    def get_phase_id(self, phase_name):
        """
        Ruft die ID einer SIA-Phase basierend auf ihrem Namen aus der Datenbank ab.

        Args:
            phase_name (str): Der Name der Phase.

        Returns:
            int: Die ID der Phase oder None, falls keine ID gefunden wird.

        Fehlerbehandlung:
        ------------------
        - Gibt None zurück, falls ein Fehler bei der Datenbankabfrage auftritt.
        """
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("SELECT phase_id FROM sia_phases WHERE phase_name = %s", (phase_name,))
                result = cursor.fetchone()
                return result[0] if result else None  # Gibt die ID zurück oder None
            except Exception as e:
                print(f"Fehler beim Abrufen der Phase ID: {e}")
                return None
            finally:
                cursor.close()
                connection.close()
        return None

    def load_soll_stunden(self):
        """
        Lädt die Sollstunden für jede Phase aus der Datenbank und zeigt sie in den Labels an.

        Fehlerbehandlung:
        ------------------
        - Zeigt "--" an, falls keine Sollstunden gefunden werden.
        - Zeigt "Fehler" an, falls ein Fehler bei der Datenbankabfrage auftritt.
        """
        if not self.project_number:
            for label in self.soll_stunden_labels.values():
                label.configure(text="")
            return

        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                for phase in self.buttons.keys():
                    query = """
                    SELECT soll_stunden FROM project_sia_phases
                    WHERE project_number = %s AND phase_name = %s
                    """
                    cursor.execute(query, (self.project_number, phase))
                    result = cursor.fetchone()
                    soll_stunden = result[0] if result else "--"
                    self.soll_stunden_labels[phase].configure(text=f"{soll_stunden}")
            except Exception as e:
                for label in self.soll_stunden_labels.values():
                    label.configure(text="Fehler")
            finally:
                cursor.close()
                connection.close()
