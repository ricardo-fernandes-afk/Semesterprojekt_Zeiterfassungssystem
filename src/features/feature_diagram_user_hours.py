import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from db.db_connection import create_connection
from gui.gui_appearance_color import appearance_color, get_default_styles

class UserHoursDiagram(ctk.CTkFrame):
    def __init__(self, master, user_id):
        self.colors = appearance_color()
        self.styles = get_default_styles()
        super().__init__(master, fg_color=self.colors["alt_background"])
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
        """Initialisiert die Diagramm-Widgets, ohne sie anzuzeigen."""
        self.figure = plt.Figure(figsize=(5, 5), dpi=100)
        self.figure.set_facecolor(self.colors["alt_background"])
        self.ax = self.figure.add_subplot(111)
        self.ax.set_facecolor(self.colors["alt_background"])
        self.canvas = FigureCanvasTkAgg(self.figure, self)
    
    def show_diagram(self):
        """Zeigt das Diagramm an."""
        self.no_data_label.pack_forget()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        
    def hide_diagram(self):
        """Versteckt das Diagramm."""
        self.canvas.get_tk_widget().pack_forget()
        self.no_data_label.pack(fill="both", expand=True)
    
    def load_daily_target(self):
        """Lädt das tägliche Ziel aus der Datenbank für den angemeldeten Benutzer."""
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
        """Lädt die Stunden für das angegebene Datum aus der Datenbank und aktualisiert das Diagramm."""
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
        """Aktualisiert das Diagramm basierend auf den übergebenen Stunden."""
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
                f"{self.current_hours:+.1f}h",
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
