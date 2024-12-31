import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from db.db_connection import create_connection
from gui.gui_appearance_color import appearance_color, get_default_styles

class ProjectPhaseDiagram(ctk.CTkFrame):
    def __init__(self, master, user_id, project_number):
        self.colors = appearance_color()
        self.styles = get_default_styles()
        super().__init__(master, corner_radius=10, fg_color=self.colors["background_light"])
        self.project_number = project_number
        self.user_id = user_id
        self.canvas = None
        self.create_widgets()
        
    def fetch_data(self):
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                query = '''
                SELECT
                    sp.phase_name,
                    sp.phase_number,
                    psp.soll_stunden,
                    COALESCE(SUM(te.hours), 0) AS total_hours,
                    COALESCE(SUM(CASE WHEN te.user_id = %s THEN te.hours ELSE 0 END), 0) AS user_hours
                FROM sia_phases sp
                LEFT JOIN project_sia_phases psp
                    ON sp.phase_name = psp.phase_name AND psp.project_number = %s
                LEFT JOIN time_entries te
                    ON sp.phase_id = te.phase_id AND te.project_number = %s
                GROUP BY sp.phase_name, sp.phase_number, psp.soll_stunden
                ORDER BY sp.phase_number;
                '''
                cursor.execute(query, (self.user_id, self.project_number, self.project_number))
                result = cursor.fetchall()
                return result
            except Exception as e:
                print(f"Fehler beim Laden der Projektphasen: {e}")
                return None
            finally:
                cursor.close()
                connection.close()
        else:
            print("Keine Verbindung zur Datenbank.")
            return None
    
    def update_widgets(self):
        data = self.fetch_data()
        if not data:
            if self.canvas:
                self.canvas.get_tk_widget().destroy()
            no_data_label = ctk.CTkLabel(self, text="Keine Daten gefunden.", **self.styles["title"])
            no_data_label.pack(fill="both", expand=True)
            print(f"Keine Daten für Projekt {self.project_number}, User {self.user_id} gefunden.")
            return
        
        phases, phase_number, soll, total, user = zip(*data)
        
        width = self.winfo_width()/100
        height = self.winfo_height()/100
        fig, ax = plt.subplots(figsize=(max(12, width), max(6, height)))
        fig.set_facecolor(self.colors["background_light"])
        ax.set_facecolor(self.colors["background_light"])
        bar_width = 0.8
        x = range(len(phases))
        
        for i, (s,t,u) in enumerate(zip(soll, total, user)):
            ax.bar(
                i,
                s,
                bar_width,
                color="none",
                edgecolor=self.colors["error"],
                linestyle="--",
                linewidth=2,
                label="Sollstunden" if i==0 else "",
                zorder=3,
            )
            ax.bar(
                i,
                t,
                bar_width,
                color=self.colors["secondary"],
                alpha=0.3,
                label="Gesamtstunden" if i==0 else "",
                zorder=1,
            )
            ax.bar(
                i,
                u,
                bar_width,
                color=self.colors["primary"],
                label="Meine Leistung" if i==0 else "",
                zorder=2,
            )
        
        ax.set_xticks(x)
        ax.set_xticklabels(phases)
        ax.tick_params(left=False, labelleft=False, bottom=True)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        
        self.canvas = FigureCanvasTkAgg(fig, self)
        self.canvas.get_tk_widget().pack(fill="both", padx=10, pady=10, expand=True)
        self.canvas.draw()
    
    def create_widgets(self):
        self.update_widgets()
    
    def refresh_chart(self):
        self.update_widgets()
        