# Datei: gui_stunden_uebersicht_frame.py
import customtkinter as ctk
from db.db_connection import create_connection
import calendar
from datetime import datetime
from tkinter import ttk

class StundenUebersichtFrame(ctk.CTkFrame):
    def __init__(self, master, project_number=None):
        super().__init__(master, corner_radius=10)
        self.project_number = project_number
        self.selected_month = datetime.now().month
        self.selected_year = datetime.now().year
        self.create_widgets()
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def create_widgets(self):
        # Filter-Dropdowns für Monat, Jahr, Benutzername und Phase
        filter_frame = ctk.CTkFrame(self)
        filter_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

        # Monat-Auswahl
        month_label = ctk.CTkLabel(filter_frame, text="Monat:")
        month_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.month_combo = ctk.CTkComboBox(filter_frame, values=list(calendar.month_name)[1:])
        self.month_combo.set(calendar.month_name[self.selected_month])
        self.month_combo.grid(row=0, column=1, padx=5, pady=5)
        
        # Jahr-Auswahl
        year_label = ctk.CTkLabel(filter_frame, text="Jahr:")
        year_label.grid(row=0, column=2, padx=5, pady=5, sticky="w")

        self.year_combo = ctk.CTkComboBox(filter_frame, values=[str(year) for year in range(2020, datetime.now().year + 1)])
        self.year_combo.set(str(self.selected_year))
        self.year_combo.grid(row=0, column=3, padx=5, pady=5)

        # Benutzername-Auswahl
        user_label = ctk.CTkLabel(filter_frame, text="Benutzername:")
        user_label.grid(row=0, column=4, padx=5, pady=5, sticky="w")

        self.user_combo = ctk.CTkComboBox(filter_frame)
        self.user_combo.grid(row=0, column=5, padx=5, pady=5)
        
        # Phase-Auswahl
        phase_label = ctk.CTkLabel(filter_frame, text="Phase:")
        phase_label.grid(row=0, column=6, padx=5, pady=5, sticky="w")

        self.phase_combo = ctk.CTkComboBox(filter_frame)
        self.phase_combo.grid(row=0, column=7, padx=5, pady=5)

        # Aktualisieren-Button
        update_button = ctk.CTkButton(filter_frame, text="Filtern", command=self.update_stunden)
        update_button.grid(row=1, columnspan=8, padx=5, pady=5)

        # Treeview für die Stundenübersicht mit Filter-Möglichkeit
        columns = ("Benutzername", "Phase", "Stunden")
        self.stunden_treeview = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.stunden_treeview.heading(col, text=col)
            self.stunden_treeview.column(col, minwidth=50, stretch=True)
        self.stunden_treeview.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")

        # Scrollbar hinzufügen
        scrollbar = ctk.CTkScrollbar(self, command=self.stunden_treeview.yview)
        self.stunden_treeview.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=2, column=1, sticky='ns')

        # Filterwerte laden
        self.load_filter_values()

        # Initiale Ansicht aktualisieren
        self.update_stunden()

    def load_filter_values(self):
        # Benutzername-Dropdown mit Werten füllen, die nur die Benutzer des aktuellen Projekts anzeigen
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("""
                    SELECT DISTINCT u.username 
                    FROM users u
                    JOIN user_projects up ON u.user_id = up.user_id
                    WHERE up.project_number = %s
                """, (self.project_number,))
                users = cursor.fetchall()
                user_names = [user[0] for user in users]
                self.user_combo.configure(values=["Alle"] + user_names)
                self.user_combo.set("Alle")
                
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

    def update_stunden(self):
        # Alte Daten entfernen
        for item in self.stunden_treeview.get_children():
            self.stunden_treeview.delete(item)
        
        # Monat, Jahr, Benutzername und Phase aus den Dropdowns abrufen
        selected_month = list(calendar.month_name).index(self.month_combo.get())
        selected_year = int(self.year_combo.get())
        selected_user = self.user_combo.get()
        selected_phase = self.phase_combo.get()

        # Datenbankabfrage zur Abrufung der Stunden basierend auf Jahr, Monat, Benutzer und Phase
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                query = """
                    SELECT u.username, s.phase_name, te.hours
                    FROM time_entries te
                    JOIN users u ON te.user_id = u.user_id
                    JOIN sia_phases s ON te.phase_id = s.phase_id
                    WHERE te.project_number = %s
                    AND EXTRACT(MONTH FROM te.entry_date) = %s
                    AND EXTRACT(YEAR FROM te.entry_date) = %s
                """
                params = [self.project_number, selected_month, selected_year]

                # Filter für Benutzername anwenden
                if selected_user != "Alle":
                    query += " AND u.username = %s"
                    params.append(selected_user)

                # Filter für Phase anwenden
                if selected_phase != "Alle":
                    query += " AND s.phase_name = %s"
                    params.append(selected_phase)

                cursor.execute(query, params)
                
                entries = cursor.fetchall()
                total_filtered_hours = 0

                # Daten in die Treeview einfügen
                for entry in entries:
                    self.stunden_treeview.insert("", "end", values=entry)
                    total_filtered_hours += entry[2]
                
                # Gesamtstunden für den Filter anzeigen
                self.stunden_treeview.insert("", "end", values=("", "Gesamtstunden (Filter)", total_filtered_hours), tags=('filter_total',))
                
                # Gesamtstunden für das gesamte Projekt abrufen
                cursor.execute("""
                    SELECT SUM(te.hours)
                    FROM time_entries te
                    WHERE te.project_number = %s
                """, (self.project_number,))
                
                total_project_hours = cursor.fetchone()[0] or 0
                self.stunden_treeview.insert("", "end", values=("", "Gesamtstunden (Projekt)", total_project_hours), tags=('project_total',))

                # Styling für die Gesamtzeilen
                self.stunden_treeview.tag_configure('filter_total', background='#d1d1d1', font=('', 10, 'bold'))
                self.stunden_treeview.tag_configure('project_total', background='#b0b0b0', font=('', 10, 'bold'))
                    
            except Exception as e:
                print(f"Fehler beim Laden der Stunden: {e}")
            
            finally:
                cursor.close()
                connection.close()
