"""
Modul: Stundenübersicht für Benutzer in TimeArch.

Dieses Modul stellt eine grafische Benutzeroberfläche bereit, um die Stundenübersicht für einen spezifischen Benutzer anzuzeigen. Es umfasst Funktionen wie Filtern nach Monat, Jahr, Projekt und Phase sowie das Exportieren der angezeigten Daten.

Klassen:
--------
- StundenUebersichtUserFrame: Hauptklasse zur Darstellung und Verwaltung der Stundenübersicht für Benutzer.

Methoden:
---------
- __init__(self, master, user_id=None): Initialisiert das Frame mit dem Benutzerkontext.
- create_widgets(self): Erstellt die Widgets für die Filter- und Stundenanzeige sowie die Exportfunktion.
- load_filter_values(self): Lädt die Werte für die Filter (Projekte und Phasen) aus der Datenbank.
- update_projects(self): Aktualisiert die Stundenübersicht basierend auf den ausgewählten Filtern.

Verwendung:
-----------
    from gui_stunden_uebersicht_user import StundenUebersichtUserFrame

    frame = StundenUebersichtUserFrame(master, user_id=1)
    frame.pack()
"""

import customtkinter as ctk
from db.db_connection import create_connection
from gui.gui_appearance_color import appearance_color, get_default_styles, apply_treeview_style
from features.feature_export import export_to_excel
import calendar
from datetime import datetime
from tkinter import ttk

class StundenUebersichtUserFrame(ctk.CTkFrame):
    """
    Eine Klasse, die die Stundenübersicht für einen Benutzer darstellt und verwaltet.

    Ermöglicht das Anzeigen und Filtern der Stunden eines Benutzers sowie den Export der gefilterten Daten.
    """
    def __init__(self, master, user_id=None):
        """
        Initialisiert das Frame für die Stundenübersicht.

        Args:
            master (ctk.CTk): Das übergeordnete Fenster.
            user_id (int, optional): Die Benutzer-ID, für die die Stundenübersicht angezeigt werden soll.
        """
        self.colors = appearance_color()
        self.styles = get_default_styles()
        
        super().__init__(master, corner_radius=10, fg_color=self.colors["alt_background"])
        self.user_id = user_id
        self.selected_month = datetime.now().month
        self.selected_year = datetime.now().year
        self.create_widgets()
        print(f"Initial user_id: {self.user_id}")

    def create_widgets(self):
        """
        Erstellt die Widgets für die Filter- und Stundenanzeige sowie die Exportfunktion.

        - Fügt Filter-Widgets für Monat, Jahr, Projekt und Phase hinzu.
        - Erstellt ein Treeview zur Anzeige der Stundenübersicht.
        - Fügt Buttons für das Aktualisieren und Exportieren hinzu.
        """
        # Filter-Dropdowns für Monat, Jahr, Projektname und Phase
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
            values= ["Alle"] + [str(year) for year in range(2024, datetime.now().year + 1)],
            **self.styles["combobox"],
        )
        self.year_combo.set(str(self.selected_year))
        self.year_combo.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        # Projekt-Auswahl
        project_label = ctk.CTkLabel(filter_frame, text="Projekt", **self.styles["text"])
        project_label.grid(row=0, column=2, padx=10, sticky="s")

        self.project_combo = ctk.CTkComboBox(filter_frame, **self.styles["combobox"])
        self.project_combo.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")
        
        # Phase-Auswahl
        phase_label = ctk.CTkLabel(filter_frame, text="Phase", **self.styles["text"])
        phase_label.grid(row=0, column=3, padx=10, sticky="s")

        self.phase_combo = ctk.CTkComboBox(filter_frame, **self.styles["combobox"])
        self.phase_combo.grid(row=1, column=3, padx=10, pady=10, sticky="nsew")

        # Aktualisieren-Button
        filter_button = ctk.CTkButton(
            filter_frame,
            text="Filtern",
            command=self.update_projects,
            **self.styles["button"],
        )
        filter_button.grid(row=2, column=0, columnspan=2, padx=10, sticky="e")
        
        export_button = ctk.CTkButton(
            filter_frame,
            text="Exportieren",
            command=lambda: export_to_excel("user", self.user_id),
            **self.styles["button_secondary"],
        )
        export_button.grid(row=2, column=2, columnspan=2, padx=10, sticky="w")

        # Treeview für die Projekteübersicht
        tree_frame = ctk.CTkFrame(self, fg_color=self.colors["alt_background"])
        tree_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        columns = ("Projekt", "Datum", "Phase", "Aktivität", "Notiz", "Stunden")
        self.project_treeview = ttk.Treeview(tree_frame, columns=columns, show="headings", height=6)
        apply_treeview_style(self.colors)
        
        for col in columns:
            self.project_treeview.heading(col, text=col)
            self.project_treeview.column(col, width=0, stretch=True)
        self.project_treeview.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Scrollbar hinzufügen
        scrollbar = ctk.CTkScrollbar(
            tree_frame,
            command=self.project_treeview.yview,
            height=6,
            fg_color=self.colors["alt_background"],
            button_color=self.colors["background_light"],
        )
        self.project_treeview.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y", anchor="e")

        # Filterwerte laden
        self.load_filter_values()

        # Initiale Ansicht aktualisieren
        self.update_projects()

    def load_filter_values(self):
        """
        Lädt die Werte für die Filter aus der Datenbank.

        - Ruft alle Projekte und Phasen ab, die dem Benutzer zugeordnet sind.
        - Füllt die Filter-Comboboxen mit den abgerufenen Werten.

        Fehlerbehandlung:
        ------------------
        - Zeigt eine Fehlermeldung an, falls die Datenbankabfrage fehlschlägt.
        """
        # Projekte-Dropdown mit Projekten des aktuellen Benutzers füllen
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("""
                    SELECT DISTINCT p.project_number, p.project_name 
                    FROM projects p
                    JOIN user_projects up ON p.project_number = up.project_number
                    WHERE up.user_id = %s
                """, (self.user_id,))
                projects = cursor.fetchall()
                project_names = [f"{project[0]} - {project[1]}" for project in projects]
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
        """
        Aktualisiert die Stundenübersicht basierend auf den ausgewählten Filtern.

        - Lädt die gefilterten Stunden aus der Datenbank.
        - Füllt das Treeview mit den abgerufenen Daten.

        Fehlerbehandlung:
        ------------------
        - Zeigt eine Fehlermeldung an, falls keine Daten gefunden werden oder die Abfrage fehlschlägt.
        """
        # Alte Daten entfernen
        for item in self.project_treeview.get_children():
            self.project_treeview.delete(item)
        
        # Monat, Jahr, Projektname und Phase aus den Dropdowns abrufen
        selected_month = self.month_combo.get()
        selected_year = self.year_combo.get()
        selected_project = self.project_combo.get()
        selected_phase = self.phase_combo.get()

        # Datenbankabfrage zur Abrufung der Projekte basierend auf Jahr, Monat, Projektname und Phase
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                query = """
                    SELECT p.project_number, p.project_name, s.phase_name, te.hours, te.entry_date, te.activity, te.note
                    FROM time_entries te
                    JOIN projects p ON te.project_number = p.project_number
                    LEFT JOIN sia_phases s ON te.phase_id = s.phase_id
                    WHERE te.user_id = %s
                """
                params = [self.user_id]
                
                if selected_year != "Alle":
                    query += " AND EXTRACT(YEAR FROM te.entry_date) = %s"
                    params.append(int(selected_year))
                
                if selected_month != "Alle":
                    query += " AND EXTRACT(MONTH FROM te.entry_date) = %s"
                    month_index = list(calendar.month_name).index(selected_month)
                    params.append(month_index)

                # Filter für Projekt anwenden
                if selected_project != "Alle":
                    project_number = selected_project.split(" - ")[0]
                    query += " AND p.project_number = %s"
                    params.append(project_number)

                # Filter für Phase anwenden
                if selected_phase != "Alle":
                    query += " AND s.phase_name = %s"
                    params.append(selected_phase)

                cursor.execute(query, params)
                
                entries = cursor.fetchall()
                
                # Sortieren der Einträge nach Datum (entry_date)
                entries.sort(key=lambda x: x[4])  # x[4] ist das Datum
            
                total_filtered_hours = 0

                # Daten in die Treeview einfügen
                for entry in entries:
                    print(f"Inserting into Treeview: {entry}")
                    combined_project = f"{entry[0]} - {entry[1]}"
                    self.project_treeview.insert("", "end", values=(combined_project, entry[4], entry[2], entry[5], entry[6], entry[3]))
                    total_filtered_hours += entry[3]
                
                # Gesamtstunden für den Filter anzeigen
                self.project_treeview.insert("", "end", values=("", "", "", "", "Filter:", total_filtered_hours), tags=('filter_total',))
                
                # Gesamtstunden für alle Projekte des Benutzers abrufen
                cursor.execute("""
                    SELECT SUM(te.hours)
                    FROM time_entries te
                    WHERE te.user_id = %s
                """, (self.user_id,))
                
                total_user_hours = cursor.fetchone()[0] or 0
                self.project_treeview.insert("", "end", values=("", "", "", "", "Benutzer:", total_user_hours), tags=('user_total',))

                # Styling für die Gesamtzeilen
                self.project_treeview.tag_configure('filter_total', background='#d1d1d1', font=('', 14, 'bold'))
                self.project_treeview.tag_configure('user_total', background='#b0b0b0', font=('', 14, 'bold'))
                    
            except Exception as e:
                print(f"Fehler beim Laden der Projekte: {e}")
            
            finally:
                cursor.close()
                connection.close()
