"""
Modul: Diagramm für Beschäftigungsprozentsatz in TimeArch.

Dieses Modul erstellt ein Diagramm, das den tatsächlichen Beschäftigungsprozentsatz eines Benutzers
im Vergleich zum erwarteten Beschäftigungsprozentsatz darstellt. Die Daten werden aus der Datenbank abgerufen,
und die Visualisierung erfolgt mit Matplotlib.

Klassen:
--------
- EmploymentPercentageDiagram: Erstellt und verwaltet das Diagramm zur Analyse des Beschäftigungsprozentsatzes.

Funktionen innerhalb der Klasse:
--------------------------------
- __init__(self, master, user_id): Initialisiert das Diagramm mit dem Benutzerkontext.
- init_diagram(self): Erstellt das Matplotlib-Diagramm und bindet es in die GUI ein.
- load_data(self): Lädt Daten aus der Datenbank, berechnet Soll- und Ist-Werte und aktualisiert das Diagramm.
- update_diagram(self, actual_percentage, expected_percentage): Aktualisiert das Diagramm mit neuen Daten.

Verwendung:
-----------
    from feature_diagram_employment_percentage import EmploymentPercentageDiagram

    diagram = EmploymentPercentageDiagram(master, user_id)
    diagram.pack()
"""
import customtkinter as ctk
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from db.db_connection import create_connection
from gui.gui_appearance_color import appearance_color, get_default_styles

class EmploymentPercentageDiagram(ctk.CTkFrame):
    """
    Eine Klasse, die ein Diagramm zur Analyse des Beschäftigungsprozentsatzes erstellt.

    Die Klasse verwendet Matplotlib, um eine visuelle Darstellung des effektiven
    Beschäftigungsprozentsatzes im Vergleich zum erwarteten Prozentsatz zu liefern.
    """
    def __init__(self, master, user_id):
        """
        Initialisiert die Diagrammklasse mit den benötigten Daten und GUI-Komponenten.

        Args:
            master (ctk.CTk): Das übergeordnete Fenster.
            user_id (int): Die Benutzer-ID, deren Beschäftigungsprozentsatz analysiert wird.
        """
        self.colors = appearance_color()
        self.styles = get_default_styles()
        super().__init__(master, corner_radius=10, fg_color=self.colors["background"])
        self.user_id = user_id

        self.init_diagram()
        self.load_data()

    def init_diagram(self):
        """
        Erstellt und initialisiert die Diagramm-Widgets.

        - Bindet Matplotlib in die GUI ein.
        - Setzt Farben und Hintergrund für das Diagramm.
        """
        self.figure = plt.Figure(figsize=(5, 5), dpi=100)
        self.figure.set_facecolor(self.colors["background"])
        self.ax = self.figure.add_subplot(111)
        self.ax.set_facecolor(self.colors["background"])
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def load_data(self):
        """
        Lädt die Daten aus der Datenbank, berechnet Soll- und Ist-Werte
        und aktualisiert das Diagramm.

        Datenbankabfragen:
        -------------------
        - Ruft die Sollstunden und den erwarteten Prozentsatz aus `user_settings` ab.
        - Berechnet die tatsächlich geleisteten Stunden aus `time_entries`.

        Fehlerbehandlung:
        ------------------
        - Zeigt eine Fehlermeldung an, falls die Daten nicht geladen werden können.
        """
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                # Abfrage der Benutzerdaten
                cursor.execute("""
                    SELECT default_hours_per_day, employment_percentage, start_date
                    FROM user_settings
                    WHERE user_id = %s
                """, (self.user_id,))
                result = cursor.fetchone()

                if not result:
                    print("Fehler: Keine Benutzerdaten gefunden.")
                    return

                default_hours_per_day, expected_percentage, start_date = result
                today = datetime.date.today()
                if start_date is None:
                    start_date = datetime.date(today.year, 1, 1)
                elif isinstance(start_date, str):
                    start_date = datetime.date.fromisoformat(start_date)

                # Arbeitstage seit Startdatum
                total_work_days = sum(1 for day in range((today - start_date).days + 1)
                                      if (start_date + datetime.timedelta(days=day)).weekday() < 5)

                # Soll-Stunden
                expected_hours = (default_hours_per_day * expected_percentage / 100) * total_work_days

                # Ist-Stunden
                current_year = datetime.date.today().year
                cursor.execute("""
                    SELECT COALESCE(SUM(hours), 0)
                    FROM time_entries
                    WHERE user_id = %s AND EXTRACT(YEAR FROM entry_date) = %s
                """, (self.user_id, current_year))
                actual_hours = cursor.fetchone()[0] or 0

                # Tatsächlicher Prozentsatz
                actual_percentage = (actual_hours / expected_hours) * 100 if expected_hours > 0 else 0

                # Diagramm aktualisieren
                self.update_diagram(actual_percentage, expected_percentage)

            except Exception as e:
                print(f"Fehler beim Laden der Daten: {e}")
            finally:
                cursor.close()
                connection.close()

    def update_diagram(self, actual_percentage, expected_percentage):
        """
        Aktualisiert das Diagramm mit den neuen Prozentsätzen.

        Args:
            actual_percentage (float): Der tatsächliche Beschäftigungsprozentsatz.
            expected_percentage (float): Der erwartete Beschäftigungsprozentsatz.

        - Passt die Farbe des Diagramms basierend auf dem Vergleich der Prozentsätze an.
        - Zeigt den tatsächlichen Prozentsatz im Diagramm an.
        """
        self.ax.clear()

        if actual_percentage < expected_percentage:
            color = self.colors["error"]
        else:
            color = self.colors["primary"]

        self.ax.pie(
            [1],
            colors=[color],
            startangle=90,
            wedgeprops={'width': 0.4},
            radius=1.5,
        )

        self.ax.text(
            0,
            0,
            f"{actual_percentage:.1f}%\nEffektiver\nStellenprozent",
            ha="center",
            va="center",
            fontsize=18,
            fontweight="bold",
            color=self.colors["text_light"],
        )

        self.canvas.draw()
