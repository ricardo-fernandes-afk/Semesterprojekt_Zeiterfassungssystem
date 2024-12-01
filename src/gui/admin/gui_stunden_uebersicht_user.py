import customtkinter as ctk
from db.db_connection import create_connection
import calendar
from datetime import datetime
from tkinter import ttk

class StundenUebersichtUserFrame(ctk.CTkFrame):
    def __init__(self, master, user_id=None):
        super().__init__(master, corner_radius=10)
        self.user_id = user_id
        self.selected_month = datetime.now().month
        self.selected_year = datetime.now().year
        self.create_widgets()

    def create_widgets(self):
        # Filter-Dropdowns für Monat, Jahr, Projektname und Phase
        filter_frame = ctk.CTkFrame(self)
        filter_frame.pack(padx=10, pady=10, fill="x")
        
        for col in range(8):
            filter_frame.grid_columnconfigure(col, weight=1)

        # Monat-Auswahl
        month_label = ctk.CTkLabel(filter_frame, text="Monat:")
        month_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.month_combo = ctk.CTkComboBox(filter_frame, values=list(calendar.month_name)[1:])
        self.month_combo.set(calendar.month_name[self.selected_month])
        self.month_combo.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        # Jahr-Auswahl
        year_label = ctk.CTkLabel(filter_frame, text="Jahr:")
        year_label.grid(row=0, column=2, padx=10, pady=10, sticky="w")

        self.year_combo = ctk.CTkComboBox(filter_frame, values=[str(year) for year in range(2024, datetime.now().year + 1)])
        self.year_combo.set(str(self.selected_year))
        self.year_combo.grid(row=0, column=3, padx=10, pady=10, sticky="nsew")

        # Projekt-Auswahl
        project_label = ctk.CTkLabel(filter_frame, text="Projekt:")
        project_label.grid(row=0, column=4, padx=10, pady=10, sticky="w")

        self.project_combo = ctk.CTkComboBox(filter_frame)
        self.project_combo.grid(row=0, column=5, padx=10, pady=10, sticky="nsew")
        
        # Phase-Auswahl
        phase_label = ctk.CTkLabel(filter_frame, text="Phase:")
        phase_label.grid(row=0, column=6, padx=10, pady=10, sticky="w")

        self.phase_combo = ctk.CTkComboBox(filter_frame)
        self.phase_combo.grid(row=0, column=7, padx=10, pady=10, sticky="nsew")

        # Aktualisieren-Button
        filter_button = ctk.CTkButton(filter_frame, text="Filtern", command=self.update_projects)
        filter_button.grid(row=1, columnspan=8, padx=10, pady=(0,10))

        # Treeview für die Projekteübersicht
        tree_frame = ctk.CTkFrame(self)
        tree_frame.pack(padx=10, pady=(0,10), fill="both", expand=True)
        
        columns = ("Projektname", "Phase", "Stunden")
        self.project_treeview = ttk.Treeview(tree_frame, columns=columns, show="headings", height=5)
        
        for col in columns:
            self.project_treeview.heading(col, text=col)
            self.project_treeview.column(col, width=100)
        self.project_treeview.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Scrollbar hinzufügen
        scrollbar = ctk.CTkScrollbar(tree_frame, command=self.project_treeview.yview, height=5)
        self.project_treeview.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y", anchor="e")

        # Filterwerte laden
        self.load_filter_values()

        # Initiale Ansicht aktualisieren
        self.update_projects()

    def load_filter_values(self):
        # Projekte-Dropdown mit Projekten des aktuellen Benutzers füllen
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("""
                    SELECT DISTINCT p.project_name 
                    FROM projects p
                    JOIN user_projects up ON p.project_number = up.project_number
                    WHERE up.user_id = %s
                """, (self.user_id,))
                projects = cursor.fetchall()
                project_names = [project[0] for project in projects]
                self.project_combo.configure(values=["Alle"] + project_names)
                self.project_combo.set("Alle")
                
                # Phase-Dropdown mit Werten füllen
                cursor.execute("SELECT DISTINCT phase_name FROM sia_phases")
                phases = cursor.fetchall()
                phase_names = [phase[0] for phase in phases]
                self.phase_combo.configure(values=["Alle"] + phase_names)
                self.phase_combo.set("Alle")
                
            except Exception as e:
                print(f"Fehler beim Laden der Filterwerte: {e}")
            finally:
                cursor.close()
                connection.close()

    def update_projects(self):
        # Alte Daten entfernen
        for item in self.project_treeview.get_children():
            self.project_treeview.delete(item)
        
        # Monat, Jahr, Projektname und Phase aus den Dropdowns abrufen
        selected_month = list(calendar.month_name).index(self.month_combo.get())
        selected_year = int(self.year_combo.get())
        selected_project = self.project_combo.get()
        selected_phase = self.phase_combo.get()

        # Datenbankabfrage zur Abrufung der Projekte basierend auf Jahr, Monat, Projektname und Phase
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                query = """
                    SELECT p.project_name, s.phase_name, te.hours
                    FROM time_entries te
                    JOIN projects p ON te.project_number = p.project_number
                    JOIN sia_phases s ON te.phase_id = s.phase_id
                    WHERE te.user_id = %s
                    AND EXTRACT(MONTH FROM te.entry_date) = %s
                    AND EXTRACT(YEAR FROM te.entry_date) = %s
                """
                params = [self.user_id, selected_month, selected_year]

                # Filter für Projekt anwenden
                if selected_project != "Alle":
                    query += " AND p.project_name = %s"
                    params.append(selected_project)

                # Filter für Phase anwenden
                if selected_phase != "Alle":
                    query += " AND s.phase_name = %s"
                    params.append(selected_phase)

                cursor.execute(query, params)
                
                entries = cursor.fetchall()
                total_filtered_hours = 0

                # Daten in die Treeview einfügen
                for entry in entries:
                    self.project_treeview.insert("", "end", values=entry)
                    total_filtered_hours += entry[2]
                
                # Gesamtstunden für den Filter anzeigen
                self.project_treeview.insert("", "end", values=("", "Gesamtstunden (Filter)", total_filtered_hours), tags=('filter_total',))
                
                # Gesamtstunden für alle Projekte des Benutzers abrufen
                cursor.execute("""
                    SELECT SUM(te.hours)
                    FROM time_entries te
                    WHERE te.user_id = %s
                """, (self.user_id,))
                
                total_user_hours = cursor.fetchone()[0] or 0
                self.project_treeview.insert("", "end", values=("", "Gesamtstunden (Benutzer)", total_user_hours), tags=('user_total',))

                # Styling für die Gesamtzeilen
                self.project_treeview.tag_configure('filter_total', background='#d1d1d1', font=('', 10, 'bold'))
                self.project_treeview.tag_configure('user_total', background='#b0b0b0', font=('', 10, 'bold'))
                    
            except Exception as e:
                print(f"Fehler beim Laden der Projekte: {e}")
            
            finally:
                cursor.close()
                connection.close()