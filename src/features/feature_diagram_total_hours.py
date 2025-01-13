"""
Modul: Diagramm für Gesamtstunden in TimeArch.

Dieses Modul erstellt ein Diagramm, das die Gesamtstunden eines Benutzers im Vergleich zu den erwarteten Stunden
anzeigt. Es visualisiert die Stundenbilanz als Differenz zwischen tatsächlichen und Sollstunden.

Klassen:
--------
- DiagramTotalHours: Erstellt und verwaltet das Diagramm für die Gesamtstunden eines Benutzers.

Funktionen innerhalb der Klasse:
--------------------------------
- __init__(self, master, user_id): Initialisiert das Diagramm mit Benutzerkontext.
- init_diagram(self): Erstellt die Diagramm-Widgets und initialisiert Matplotlib.
- load_data(self): Lädt Daten aus der Datenbank, berechnet Sollstunden, tatsächliche Stunden und die Stundenbilanz.
- update_diagram(self, total_hours): Aktualisiert das Diagramm basierend auf der Stundenbilanz.

Verwendung:
-----------
    from feature_diagram_total_hours import DiagramTotalHours

    diagram = DiagramTotalHours(master, user_id)
    diagram.pack()
"""

import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from db.db_connection import create_connection
from gui.gui_appearance_color import appearance_color, get_default_styles

class DiagramTotalHours(ctk.CTkFrame):
    """
    Eine Klasse, die ein Diagramm für die Gesamtstunden eines Benutzers erstellt.

    Diese Klasse zeigt die Differenz zwischen den Sollstunden und den tatsächlichen Stunden
    in einer grafischen Darstellung an.
    """
    def __init__(self, master, user_id):
        """
        Initialisiert die Diagrammklasse mit Benutzerkontext und GUI-Komponenten.

        Args:
            master (ctk.CTk): Das übergeordnete Fenster.
            user_id (int): Die Benutzer-ID, deren Gesamtstunden angezeigt werden.
        """
        self.colors = appearance_color()
        self.styles = get_default_styles()
        super().__init__(master, corner_radius=10, fg_color=self.colors["background"])
        self.user_id = user_id

        self.init_diagram()
        self.load_data()

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
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def load_data(self):
        """
        Lädt Daten aus der Datenbank, berechnet Sollstunden, tatsächliche Stunden und die Stundenbilanz.

        Datenbankabfragen:
        -------------------
        - Ruft Sollstunden und tatsächliche Stunden für den Benutzer ab.

        Berechnungen:
        --------------
        - Sollstunden: Basierend auf dem Beschäftigungsprozentsatz und der Arbeitszeit.
        - Tatsächliche Stunden: Summiert die Stunden aus `time_entries`.

        Fehlerbehandlung:
        ------------------
        - Zeigt eine Fehlermeldung an, falls die Daten nicht geladen werden können.
        """
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                # Abfrage: Stunden pro Tag, Beschäftigungsprozentsatz, und tatsächliche Stunden
                cursor.execute("""
                    SELECT default_hours_per_day, employment_percentage, start_date
                    FROM user_settings
                    WHERE user_id = %s
                """, (self.user_id,))
                result = cursor.fetchone()

                if not result:
                    print("Keine Daten für diesen Benutzer gefunden.")
                    self.update_diagram(None)
                    return

                default_hours_per_day, employment_percentage, start_date = result

                # Arbeitstage seit Startdatum berechnen
                import datetime
                today = datetime.date.today()
                if start_date is None:
                    start_date = datetime.date(today.year, 1, 1)
                elif isinstance(start_date, str):
                    start_date = datetime.date.fromisoformat(start_date)

                total_work_days = [(start_date + datetime.timedelta(days=day)) for day in range((today - start_date).days + 1) if (start_date + datetime.timedelta(days=day)).weekday() < 5]

                # Sollstunden berechnen
                expected_hours = (default_hours_per_day * employment_percentage / 100) * len(total_work_days)

                # Tatsächliche Arbeitsstunden abrufen
                cursor.execute("""
                    SELECT entry_date, COALESCE(SUM(hours), 0)
                    FROM time_entries
                    WHERE user_id = %s AND entry_date >= %s
                    GROUP BY entry_date
                """, (self.user_id, start_date))
                entries = dict(cursor.fetchall())
                
                actual_hours = sum(entries.get(day, 0) for day in total_work_days)

                # Differenz berechnen
                total_hours = actual_hours - expected_hours

                # Diagramm aktualisieren
                self.update_diagram(total_hours)

            except Exception as e:
                print(f"Fehler beim Laden der Daten: {e}")
                self.update_diagram(None)
            finally:
                cursor.close()
                connection.close()

    def update_diagram(self, total_hours):
        """
        Aktualisiert das Diagramm basierend auf den tatsächlichen und erwarteten Stunden.

        Args:
            total_hours (float): Die tatsächlich geleisteten Stunden.
            expected_hours (float): Die erwarteten Sollstunden.

        - Zeigt die Stundenbilanz im Diagramm an.
        - Passt die Farben basierend auf der Differenz an (positiv/negativ).
        """
        self.ax.clear()

        if total_hours is None:
            return  # Diagramm bleibt leer

        if total_hours < 0:
            color = self.colors["error"]  # Rot für Minus
        else:
            color = self.colors["primary"]  # Grün für 0 oder mehr

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
            f"{total_hours:+.2f}h\nStundenbilanz",
            ha="center",
            va="center",
            fontsize=18,
            fontweight="bold",
            color=self.colors["text_light"],
        )

        self.canvas.draw()
