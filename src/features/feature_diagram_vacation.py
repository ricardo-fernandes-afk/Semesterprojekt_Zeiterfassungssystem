import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from db.db_connection import create_connection
from gui.gui_appearance_color import appearance_color, get_default_styles

class VacationDiagram(ctk.CTkFrame):
    def __init__(self, master, user_id):
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
        """Initialisiert die Diagramm-Komponenten."""
        self.figure = plt.Figure(figsize=(5, 5), dpi=100)
        self.figure.set_facecolor(self.colors["background"])
        self.ax = self.figure.add_subplot(111)
        self.ax.set_facecolor(self.colors["background"])

        # Matplotlib Canvas erstellen
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill="both", expand=True)

    def load_vacation_data(self):
        """Lädt die Urlaubsdaten für den Benutzer."""
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
        """Aktualisiert das Diagramm basierend auf den geladenen Daten."""
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
