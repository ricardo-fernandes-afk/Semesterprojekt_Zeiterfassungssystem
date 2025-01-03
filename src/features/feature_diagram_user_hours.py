"""
Modul: Diagramm für Benutzerstunden in TimeArch.

Dieses Modul erstellt ein Kreisdiagramm, das die Tagesstunden eines Benutzers darstellt. Es visualisiert die
Differenz zwischen dem Tagesziel und den tatsächlich erfassten Stunden.

Klassen:
--------
- UserHoursDiagram: Erstellt und verwaltet das Diagramm für die Benutzerstunden.

Funktionen innerhalb der Klasse:
--------------------------------
- __init__(self, master, user_id): Initialisiert das Diagramm mit Benutzerkontext.
- init_diagram(self): Erstellt die Diagramm-Widgets und initialisiert Matplotlib.
- show_diagram(self): Zeigt das Diagramm-Widget an.
- hide_diagram(self): Versteckt das Diagramm-Widget.
- load_daily_target(self): Lädt das Tagesziel (Sollstunden) aus der Datenbank.
- load_hours_from_db(self, selected_date): Lädt die Stunden eines Benutzers für ein bestimmtes Datum aus der Datenbank.
- update_diagram(self, hours): Aktualisiert das Diagramm basierend auf den geladenen Stunden.
- refresh_diagram(self, selected_date=None): Aktualisiert das Diagramm basierend auf dem ausgewählten Datum.

Verwendung:
-----------
    from feature_diagram_user_hours import UserHoursDiagram

    diagram = UserHoursDiagram(master, user_id)
    diagram.pack()
"""

import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from db.db_connection import create_connection
from gui.gui_appearance_color import appearance_color, get_default_styles

class UserHoursDiagram(ctk.CTkFrame):
    """
    Eine Klasse, die ein Diagramm zur Visualisierung der Tagesstunden eines Benutzers erstellt.

    Diese Klasse zeigt die Differenz zwischen dem Tagesziel (Sollstunden) und den tatsächlich
    erfassten Stunden für ein bestimmtes Datum.
    """
    def __init__(self, master, user_id):
        """
        Initialisiert die Diagrammklasse mit Benutzerkontext und GUI-Komponenten.

        Args:
            master (ctk.CTk): Das übergeordnete Fenster.
            user_id (int): Die Benutzer-ID, deren Tagesstunden angezeigt werden.
        """
        self.colors = appearance_color()
        self.styles = get_default_styles()
        super().__init__(master, corner_radius=10, fg_color=self.colors["background"])
        self.user_id = user_id
        self.daily_target = None  # Standardwert, falls keine Datenbankverbindung besteht
        self.current_hours = None
        
        # Text für den leeren Zustand
        self.no_data_label = ctk.CTkLabel(self, text="Datum auswählen", **self.styles["title"])
        self.no_data_label.pack(fill="both", expand=True)
        
        # Initialisiere die Diagramm-Widgets
        self.init_diagram()
        
        # Lade das tägliche Ziel aus der Datenbank
        self.load_daily_target()
                
    def init_diagram(self):
        """
        Erstellt die Diagramm-Widgets und initialisiert Matplotlib.

        - Setzt die Farben und das Layout für das Diagramm.
        - Bindet das Diagramm in die GUI ein.
        """
        self.figure = plt.Figure(figsize=(5, 5), dpi=100)
        self.figure.set_facecolor(self.colors["background"])
        self.ax = self.figure.add_subplot(111)
        self.ax.set_facecolor(self.colors["background"])
        self.canvas = FigureCanvasTkAgg(self.figure, self)
    
    def show_diagram(self):
        """
        Zeigt das Diagramm an und versteckt den "Keine Daten"-Text.
        """
        self.no_data_label.pack_forget()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        
    def hide_diagram(self):
        """
        Versteckt das Diagramm und zeigt den "Keine Daten"-Text.
        """
        self.canvas.get_tk_widget().pack_forget()
        self.no_data_label.pack(fill="both", expand=True)
    
    def load_daily_target(self):
        """
        Lädt die Stunden eines Benutzers für ein bestimmtes Datum aus der Datenbank.

        Args:
            selected_date (str): Das ausgewählte Datum im Format YYYY-MM-DD.

        - Berechnet die Differenz zwischen Sollstunden und tatsächlich erfassten Stunden.
        - Aktualisiert das Diagramm basierend auf den geladenen Stunden.
        """
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                query = """
                SELECT default_hours_per_day
                FROM user_settings
                WHERE user_id = %s
                """
                cursor.execute(query, (self.user_id,))
                result = cursor.fetchone()
                
                if result is None or result[0] is None:
                    print(f"Fehler: Kein Daily Target für Benutzer {self.user_id} in der Datenbank gefunden.")
                    return
                
                self.daily_target = result[0]
                print(f"DEBUG: Daily target für Benutzer {self.user_id}: {self.daily_target}")
            except Exception as e:
                print(f"Fehler beim Laden des Daily Target: {e}")
            finally:
                cursor.close()
                connection.close()

    def load_hours_from_db(self, selected_date):
        """
        Aktualisiert das Diagramm basierend auf den übergebenen Stunden.

        Args:
            hours (float): Die Differenz zwischen Sollstunden und tatsächlich erfassten Stunden.

        - Passt die Farben des Diagramms basierend auf der Differenz an.
        - Zeigt den Stundenwert im Diagramm an.
        """
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                query = """
                SELECT COALESCE(SUM(hours), 0)
                FROM time_entries
                WHERE user_id = %s AND entry_date = %s
                """
                cursor.execute(query, (self.user_id, selected_date))
                total_hours = cursor.fetchone()[0]
                print(f"DEBUG: Geladene Stunden für {selected_date}: {total_hours}")
                
                self.current_hours = total_hours - self.daily_target
                print(f"DEBUG: Aktualisiere Stunden auf {self.current_hours}")
                
                self.show_diagram()
                self.update_diagram(self.current_hours)
            except Exception as e:
                print(f"Fehler beim Laden der Stunden: {e}")
                self.hide_diagram()
            finally:
                cursor.close()
                connection.close()

    def update_diagram(self, hours):
        """
        Aktualisiert das Diagramm basierend auf dem ausgewählten Datum.

        Args:
            selected_date (str, optional): Das Datum, für das die Stunden angezeigt werden sollen.

        - Lädt die Stunden für das angegebene Datum und aktualisiert das Diagramm.
        - Zeigt eine Fehlermeldung, falls kein Datum angegeben wird.
        """
        if self.daily_target is None:
            print("Fehler: Daily Target nicht geladen.")
            self.ax.clear()
            self.ax.text(0, 0, "Fehler", ha='center', va='center', fontsize=14)
            self.canvas.draw()
            return
        
        print(f"DEBUG: Stunden für Diagramm: {hours}")

        try:
            if hours < 0:
                red = abs(hours) / abs(self.daily_target)
                blue = 1 - red
                green = 0
                print(f"DEBUG: Defizit - Rot: {red}, Blau: {blue}, Grün: {green}")
            elif hours == 0:
                red = 0
                blue = 1
                green = 0
                print(f"DEBUG: Ziel erreicht - Rot: {red}, Blau: {blue}, Grün: {green}")
            else:
                red = 0
                green = abs(hours) / abs(self.daily_target)
                blue = 1 - green
                print(f"DEBUG: Überstunden - Rot: {red}, Blau: {blue}, Grün: {green}")
            
            data = [max(0,red), max(0,blue), max(0,green)]
            colors = [self.colors["error"], self.colors["secondary"], self.colors["primary"]]
            
            # Kreisdiagramm erstellen
            self.ax.clear()
            self.ax.pie(
                data,
                colors=colors,
                startangle=90,
                wedgeprops={'width': 0.4},
                radius=1.5,
            )
            # Text in der Mitte
            self.ax.text(
                0,
                0,
                f"{self.current_hours:+.1f}h\nTagesziel",
                ha='center',
                va='center',
                fontsize=18,
                fontweight='bold',
                color=self.colors["text_light"],
            )

        except Exception as e:
            print(f"Fehler beim Erstellen des Diagramms: {e}")
            self.ax.text(0, 0, "Fehler", ha='center', va='center', fontsize=14)

        self.canvas.draw()
        
    def refresh_diagram(self, selected_date=None):
        if selected_date:
            self.load_hours_from_db(selected_date)
        else:
            print("Kein Datum zum Aktualisieren des Diagramms angegeben.")
