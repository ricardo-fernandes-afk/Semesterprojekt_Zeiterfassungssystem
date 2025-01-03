"""
Modul: Admin-Projektdiagramme für TimeArch.

Dieses Modul erstellt Diagramme zur Visualisierung von Arbeitsstunden und Sollstunden für Projekte.
Die Diagramme werden basierend auf den vom Benutzer ausgewählten Filtern generiert.

Klassen:
--------
- AdminProjectDiagram: Erstellt und verwaltet Diagramme für die Projektanalyse.

Funktionen innerhalb der Klasse:
--------------------------------
- __init__(self, master, project_number, filter_frame=None): Initialisiert die Diagrammklasse.
- fetch_filtered_data(self): Ruft die Daten basierend auf den gesetzten Filtern ab.
- update_chart(self): Aktualisiert das Diagramm basierend auf den abgerufenen Daten.
- create_widgets(self): Erstellt die initialen Diagrammelemente.
- refresh_chart(self): Aktualisiert das Diagramm, um Änderungen widerzuspiegeln.

Verwendung:
-----------
    from feature_diagram_admin_project import AdminProjectDiagram

    diagram = AdminProjectDiagram(master, project_number, filter_frame)
    diagram.pack()
"""
import customtkinter as ctk
import calendar
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from db.db_connection import create_connection
from gui.gui_appearance_color import appearance_color, get_default_styles

class AdminProjectDiagram(ctk.CTkFrame):
    """
    Eine Klasse, um Diagramme zur Projektanalyse für den Admin zu erstellen.

    Diese Klasse generiert Diagramme basierend auf Projekt- und Filterdaten, einschließlich
    Sollstunden und tatsächlicher Arbeitsstunden pro Benutzer und Phase.
    """
    def __init__(self, master, project_number, filter_frame=None):
        """
        Initialisiert die Diagrammklasse mit dem übergeordneten Fenster und den Projektfiltern.

        Args:
            master (ctk.CTk): Das übergeordnete Fenster.
            project_number (str): Die Projektnummer, für die das Diagramm erstellt wird.
            filter_frame (ctk.CTkFrame, optional): Ein Frame mit Filteroptionen (Monat, Jahr, Benutzer, Phase).
        """
        self.colors = appearance_color()
        self.styles = get_default_styles()
        super().__init__(master, corner_radius=10, fg_color=self.colors["background"])
        self.project_number = project_number
        self.filter_frame = filter_frame  # Verbindung zum Filter
        self.canvas = None
        self.create_widgets()

    def fetch_filtered_data(self):
        """
        Ruft die gefilterten Daten basierend auf den Filteroptionen ab.

        Returns:
            list: Eine Liste mit den abgerufenen Datenzeilen aus der Datenbank.

        Fehlerbehandlung:
        ------------------
        - Gibt eine leere Liste zurück, wenn keine Verbindung zur Datenbank hergestellt werden kann
          oder die Filterung fehlschlägt.
        """
        if not self.filter_frame:
            print("Keine Filterwerte vorhanden.")
            return []

        # Filterwerte abrufen
        selected_month = self.filter_frame.month_combo.get()
        selected_year = int(self.filter_frame.year_combo.get())
        selected_user = self.filter_frame.user_combo.get()
        selected_phase = self.filter_frame.phase_combo.get()

        # SQL-Abfrage erstellen
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                query = """
                SELECT
                    sp.phase_name,
                    sp.phase_number,
                    psp.soll_stunden,
                    te.user_id,
                    (SELECT username FROM users WHERE user_id = te.user_id) AS username,
                    COALESCE(SUM(te.hours), 0) AS user_hours
                FROM sia_phases sp
                LEFT JOIN project_sia_phases psp
                    ON sp.phase_name = psp.phase_name AND psp.project_number = %s
                LEFT JOIN time_entries te
                    ON sp.phase_id = te.phase_id AND te.project_number = %s
                WHERE EXTRACT(YEAR FROM te.entry_date) = %s
                """
                params = [self.project_number, self.project_number, selected_year]

                # Monat-Filter hinzufügen
                if selected_month != "Alle":
                    query += " AND EXTRACT(MONTH FROM te.entry_date) = %s"
                    month_index = list(calendar.month_name).index(selected_month)
                    params.append(month_index)

                # Benutzername-Filter hinzufügen
                if selected_user != "Alle":
                    query += " AND te.user_id = (SELECT user_id FROM users WHERE username = %s)"
                    params.append(selected_user)

                # Phase-Filter hinzufügen
                if selected_phase != "Alle":
                    query += " AND sp.phase_name = %s"
                    params.append(selected_phase)

                query += """
                GROUP BY sp.phase_name, sp.phase_number, psp.soll_stunden, te.user_id, username
                ORDER BY sp.phase_number, te.user_id;
                """
                cursor.execute(query, params)
                result = cursor.fetchall()
                return result

            except Exception as e:
                print(f"Fehler beim Abrufen der gefilterten Daten: {e}")
                return []
            finally:
                cursor.close()
                connection.close()
        else:
            print("Keine Verbindung zur Datenbank.")
            return []

    def update_chart(self):
        """
        Aktualisiert das Diagramm basierend auf den abgerufenen Filterdaten.

        - Zeichnet ein Balkendiagramm mit Sollstunden und tatsächlichen Arbeitsstunden pro Phase und Benutzer.
        - Verwendet verschiedene Farben, um Benutzer im Diagramm zu unterscheiden.
        """
        data = self.fetch_filtered_data()
        
        # Datenverarbeitung (wie zuvor)
        phases = []
        users = set()
        hours_by_user = {}
        soll_hours = {}
        user_names = {}

        for row in data:
            phase_name, phase_number, soll, user_id, username, user_hours = row
            if phase_name not in phases:
                phases.append(phase_name)
            if user_id:
                users.add(user_id)
                user_names[user_id] = username
            if phase_name not in hours_by_user:
                hours_by_user[phase_name] = {}
            if user_id:
                hours_by_user[phase_name][user_id] = user_hours
            soll_hours[phase_name] = soll

        # Farbzuteilung für Benutzer
        user_colors = {user: plt.cm.tab20(i % 20) for i, user in enumerate(users)}

        fig, ax = plt.subplots(figsize=(6, 4))
        fig.patch.set_facecolor(self.colors["background"])
        ax.set_facecolor(self.colors["background"])
        bar_width = 0.8
        x = range(len(phases))

        # Soll-Stunden
        for i, phase in enumerate(phases):
            ax.bar(
                i,
                soll_hours[phase],
                bar_width,
                color="none",
                edgecolor="red",
                linestyle="--",
                linewidth=2,
                label="Sollstunden" if i == 0 else "",
                zorder=2,
            )

        # Stunden pro Benutzer
        added_labels = set()
        for user_id in users:
            y_offset = [0] * len(phases)
            for i, phase in enumerate(phases):
                user_hours = hours_by_user[phase].get(user_id, 0)
                ax.bar(
                    i,
                    user_hours,
                    bar_width,
                    bottom=y_offset[i],
                    color=user_colors[user_id],
                    label=user_names[user_id] if user_id not in added_labels else "",
                    zorder=1,
                )
                y_offset[i] += user_hours
            added_labels.add(user_id)

        ax.set_xticks(x)
        ax.set_xticklabels(phases, fontsize=10, fontweight="bold", color=self.colors["text_light"])
        ax.tick_params(left=False, labelleft=False, bottom=True)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        
        handles, labels = ax.get_legend_handles_labels()
        unique_labels = []
        unique_handles = []
        for handle, label in zip(handles, labels):
            if label not in unique_labels:
                unique_labels.append(label)
                unique_handles.append(handle)
        ax.legend(unique_handles, unique_labels)

        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        self.canvas = FigureCanvasTkAgg(fig, self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        self.canvas.draw()
    
    def create_widgets(self):
        """
        Erstellt die initialen Widgets und generiert das erste Diagramm.
        """
        self.update_chart()
    
    def refresh_chart(self):
        """
        Aktualisiert das Diagramm, um Änderungen durch Filter oder Daten widerzuspiegeln.
        """
        self.update_chart()

        
        

