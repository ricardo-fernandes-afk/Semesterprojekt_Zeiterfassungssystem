"""
Modul: Diagramm für Urlaubstage in TimeArch.

Dieses Modul erstellt ein Kreisdiagramm, das die zugewiesenen und genutzten Urlaubstage eines Benutzers darstellt.
Es zeigt ebenfalls überschrittene Urlaubstage und verbleibende Urlaubstage an.

Klassen:
--------
- VacationDiagram: Erstellt und verwaltet das Diagramm für Urlaubstage.

Funktionen innerhalb der Klasse:
--------------------------------
- __init__(self, master, user_id): Initialisiert die Diagrammklasse mit Benutzerkontext.
- init_diagram(self): Erstellt die Diagramm-Widgets und initialisiert Matplotlib.
- load_vacation_data(self): Lädt die Urlaubsdaten (zugewiesen, genutzt, verbleibend) aus der Datenbank.
- update_diagram(self): Aktualisiert das Diagramm basierend auf den geladenen Urlaubsdaten.

Verwendung:
-----------
    from feature_diagram_vacation import VacationDiagram

    diagram = VacationDiagram(master, user_id)
    diagram.pack()
"""

import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from db.db_connection import create_connection
from gui.gui_appearance_color import appearance_color, get_default_styles

class VacationDiagram(ctk.CTkFrame):
    """
    Eine Klasse, die ein Diagramm für die Urlaubstage eines Benutzers erstellt.

    Die Klasse zeigt die zugewiesenen Urlaubstage, genutzten Urlaubstage sowie überschrittene
    oder verbleibende Urlaubstage in einem Kreisdiagramm an.
    """
    def __init__(self, master, user_id):
        """
        Initialisiert die Diagrammklasse mit Benutzerkontext und GUI-Komponenten.

        Args:
            master (ctk.CTk): Das übergeordnete Fenster.
            user_id (int): Die Benutzer-ID, deren Urlaubstage angezeigt werden.
        """
        self.colors = appearance_color()
        self.styles = get_default_styles()
        super().__init__(master, corner_radius=10, fg_color=self.colors["background"])
        self.user_id = user_id
        self.assigned_vacation = None  # Vom Admin zugewiesene Urlaubstage
        self.used_vacation = None  # Genutzte Urlaubstage

        # Diagramm-Widgets initialisieren
        self.init_diagram()
        self.load_vacation_data()

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

        # Matplotlib Canvas erstellen
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill="both", expand=True)

    def load_vacation_data(self):
        """
        Lädt die Urlaubsdaten (zugewiesen, genutzt, verbleibend) für den Benutzer aus der Datenbank.

        - Zuweisung der Urlaubstage: Wird aus `user_settings` abgerufen.
        - Genutzte Urlaubstage: Summiert die Stunden aus `time_entries` mit der Aktivität 'Ferien'.
        - Berechnet verbleibende oder überschrittene Urlaubstage.

        Fehlerbehandlung:
        ------------------
        - Zeigt eine Fehlermeldung im Diagramm an, falls die Daten nicht geladen werden können.
        """
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                # Abfrage: Default Stunden pro Tag
                cursor.execute("""
                    SELECT default_hours_per_day
                    FROM user_settings
                    WHERE user_id = %s
                """, (self.user_id,))
                self.default_hours_per_day = cursor.fetchone()[0]
                # Abfrage: Zuweisung von Urlaubstagen
                cursor.execute("""
                    SELECT vacation_hours
                    FROM user_settings
                    WHERE user_id = %s
                """, (self.user_id,))
                self.assigned_vacation = cursor.fetchone()[0]

                # Abfrage: Genutzte Urlaubstage
                cursor.execute("""
                    SELECT COALESCE(SUM(hours), 0)
                    FROM time_entries
                    WHERE user_id = %s AND activity = 'Ferien'
                """, (self.user_id,))
                self.used_vacation = cursor.fetchone()[0] or 0

                self.update_diagram()

            except Exception as e:
                print(f"Fehler beim Laden der Urlaubsdaten: {e}")
                self.ax.clear()
                self.ax.text(0.5, 0.5, "Fehler beim Laden", ha="center", va="center", fontsize=12)
                self.canvas.draw()
            finally:
                cursor.close()
                connection.close()

    def update_diagram(self):
        """
        Aktualisiert das Diagramm basierend auf den geladenen Urlaubsdaten.

        - Zeichnet ein Kreisdiagramm mit genutzten, verbleibenden und überschrittenen Urlaubstagen.
        - Zeigt die Differenz (gesamt genutzte Urlaubstage - zugewiesene Urlaubstage) im Diagrammzentrum an.
        """
        assigned_vacation_days = self.assigned_vacation / self.default_hours_per_day
        used_vacation_days = self.used_vacation / self.default_hours_per_day
        
        overused = max(0, used_vacation_days - assigned_vacation_days)
        remaining = max(0, assigned_vacation_days - used_vacation_days)
        total_vacation = used_vacation_days - assigned_vacation_days

        sizes = [used_vacation_days, overused, remaining]
        colors = [self.colors["secondary"], self.colors["error"], self.colors["primary"]]

        # Diagramm zeichnen
        self.ax.clear()
        self.ax.pie(
            sizes,
            colors=colors,
            startangle=90,
            counterclock=False,
            wedgeprops={'width': 0.4},
            radius=1.5,
        )
        
        rounded_vacation = round(total_vacation, 1)
        self.ax.text(
            0,
            0,
            f"{rounded_vacation}\nUrlaubstage",
            ha="center",
            va="center",
            fontsize=18,
            fontweight="bold",
            color=self.colors["text_light"],
        )
        
        # Aktualisiere das Canvas
        self.canvas.draw()
