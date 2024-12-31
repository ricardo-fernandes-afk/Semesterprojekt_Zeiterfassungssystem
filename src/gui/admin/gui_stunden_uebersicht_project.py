# Datei: gui_stunden_uebersicht_frame.py
import customtkinter as ctk
from db.db_connection import create_connection
from gui.gui_appearance_color import appearance_color, get_default_styles, apply_treeview_style
import calendar
from datetime import datetime
from tkinter import ttk

class StundenUebersichtProjectFrame(ctk.CTkFrame):
    def __init__(self, master, project_number=None):
        self.colors = appearance_color()
        self.styles = get_default_styles()
        
        super().__init__(master, corner_radius=10, fg_color=self.colors["alt_background"])
        self.project_number = project_number
        self.selected_month = datetime.now().month
        self.selected_year = datetime.now().year
        self.create_widgets()

    def create_widgets(self):
        # Filter-Dropdowns für Monat, Jahr, Benutzername und Phase
        filter_frame = ctk.CTkFrame(self, fg_color=self.colors["alt_background"])
        filter_frame.pack(padx=10, pady=10, fill="x")
        
        for col in range(4):
            filter_frame.grid_columnconfigure(col, weight=1)

        # Monat-Auswahl
        month_label = ctk.CTkLabel(filter_frame, text="Monat", **self.styles["text"])
        month_label.grid(row=0, column=0, padx=10, sticky="s")

        self.month_combo = ctk.CTkComboBox(
            filter_frame,
            values=["Alle"] + list(calendar.month_name)[1:],
            **self.styles["combobox"],
        )
        self.month_combo.set("Alle")
        self.month_combo.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        # Jahr-Auswahl
        year_label = ctk.CTkLabel(filter_frame, text="Jahr", **self.styles["text"])
        year_label.grid(row=0, column=1, padx=10, sticky="s")

        self.year_combo = ctk.CTkComboBox(
            filter_frame,
            values=[str(year) for year in range(2024, datetime.now().year + 1)],
            **self.styles["combobox"],
        )
        self.year_combo.set(str(self.selected_year))
        self.year_combo.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        # Benutzername-Auswahl
        user_label = ctk.CTkLabel(filter_frame, text="Benutzername", **self.styles["text"])
        user_label.grid(row=0, column=2, padx=10, sticky="s")

        self.user_combo = ctk.CTkComboBox(filter_frame, **self.styles["combobox"])
        self.user_combo.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")
        
        # Phase-Auswahl
        phase_label = ctk.CTkLabel(filter_frame, text="Phase", **self.styles["text"])
        phase_label.grid(row=0, column=3, padx=10, sticky="s")

        self.phase_combo = ctk.CTkComboBox(filter_frame, **self.styles["combobox"])
        self.phase_combo.grid(row=1, column=3, padx=10, pady=10, sticky="nsew")

        # Aktualisieren-Button
        filter_button = ctk.CTkButton(
            filter_frame,
            text="Filtern",
            command= lambda: [self.update_stunden(), self.master.diagram_frame.refresh_chart()],
            **self.styles["button"],
        )
        filter_button.grid(row=2, columnspan=4, padx=10)

        # Treeview für die Stundenübersicht mit Filter-Möglichkeit
        tree_frame = ctk.CTkFrame(self, fg_color=self.colors["alt_background"])
        tree_frame.pack(padx=10, pady=(0,10), fill="both", expand=True)
        
        columns = ("Benutzername", "Datum", "Phase", "Aktivität", "Notiz", "Stunden")
        self.stunden_treeview = ttk.Treeview(tree_frame, columns=columns, show="headings", height=6)
        apply_treeview_style(self.colors)
        
        for col in columns:
            self.stunden_treeview.heading(col, text=col)
            self.stunden_treeview.column(col, width=0, stretch=True)
        self.stunden_treeview.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Scrollbar hinzufügen
        scrollbar = ctk.CTkScrollbar(
            tree_frame,
            command=self.stunden_treeview.yview,
            height=6,
            fg_color=self.colors["alt_background"],
            button_color=self.colors["background_light"],
        )
        self.stunden_treeview.configure(yscrollc=scrollbar.set)
        scrollbar.pack(side="right", fill="y", anchor="e")

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
        selected_month = self.month_combo.get()
        selected_year = int(self.year_combo.get())
        selected_user = self.user_combo.get()
        selected_phase = self.phase_combo.get()

        # Datenbankabfrage zur Abrufung der Stunden basierend auf Jahr, Monat, Benutzer und Phase
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                query = """
                SELECT u.username, s.phase_name, te.hours, te.entry_date, te.activity, te.note
                FROM time_entries te
                JOIN users u ON te.user_id = u.user_id
                LEFT JOIN sia_phases s ON te.phase_id = s.phase_id
                WHERE te.project_number = %s
                AND EXTRACT(YEAR FROM te.entry_date) = %s
                """
                params = [self.project_number, selected_year]
                
                if selected_month != "Alle":
                    query += " AND EXTRACT(MONTH FROM te.entry_date) = %s"
                    month_index = list(calendar.month_name).index(selected_month)
                    params.append(month_index)

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
                
                # Sortieren der Einträge nach Datum (entry_date)
                entries.sort(key=lambda x: x[3])
                
                total_filtered_hours = 0

                # Daten in die Treeview einfügen
                for entry in entries:
                    self.stunden_treeview.insert("", "end", values=(entry[0], entry[3], entry[1], entry[4], entry[5], entry[2]))
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
                self.stunden_treeview.tag_configure('filter_total', background='#d1d1d1', font=('', 14, 'bold'))
                self.stunden_treeview.tag_configure('project_total', background='#b0b0b0', font=('', 14, 'bold'))
                    
            except Exception as e:
                print(f"Fehler beim Laden der Stunden: {e}")
            
            finally:
                cursor.close()
                connection.close()
