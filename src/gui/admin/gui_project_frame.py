"""
Modul: Projekt-Frame für TimeArch.

Dieses Modul stellt die grafische Benutzeroberfläche zur Verwaltung von Projekten bereit. Es umfasst Funktionen
zum Hinzufügen, Löschen und Anzeigen von Projekten in einer Tabelle mit Unterstützung für Scrollbars und dynamische
Spaltenbreiten.

Klassen:
--------
- ProjectFrame: Hauptklasse für die Verwaltung von Projekten in der Admin-GUI.

Methoden:
---------
- __init__(self, master): Initialisiert das Projekt-Frame mit allen erforderlichen Widgets und Layouts.
- get_selected_project_number(self): Gibt die Nummer und den Namen des aktuell ausgewählten Projekts zurück.
- load_projects(self): Lädt alle Projekte aus der Datenbank und zeigt sie in der Tabelle an.
- open_add_project_window(self): Öffnet das Fenster zum Hinzufügen eines neuen Projekts.
- open_delete_project_window(self): Öffnet das Fenster zum Löschen eines Projekts und bestätigt die Aktion.

Verwendung:
-----------
    from gui_project_frame import ProjectFrame

    frame = ProjectFrame(master)
    frame.pack()
"""

import customtkinter as ctk
from tkinter import messagebox, ttk
from db.db_connection import create_connection
from features.feature_add_projects import add_project
from features.feature_delete_project import delete_project, get_selected_project_number
from gui.gui_appearance_color import appearance_color, get_default_styles, apply_treeview_style
 
class ProjectFrame(ctk.CTkFrame):
    """
    Eine Klasse, die ein GUI-Frame zur Verwaltung von Projekten bereitstellt.

    Funktionen:
    - Zeigt Projekte in einer Tabelle an.
    - Ermöglicht das Hinzufügen und Löschen von Projekten.
    """
    def __init__(self, master):
        """
        Initialisiert das Projekt-Frame und erstellt die GUI-Elemente.

        Args:
            master (ctk.CTk): Das übergeordnete Fenster, in dem das Frame eingebettet ist.
        """
        self.colors = appearance_color()
        self.styles = get_default_styles()
        
        super().__init__(master, corner_radius=10, fg_color=self.colors["background"])
        self.grid_propagate(False)
    
        # Label für Projekte
        project_label = ctk.CTkLabel(master=self, text="Projekte", **self.styles["title"])
        project_label.pack(pady=10, anchor="n")
        
        # Liste der Projekte
        tree_frame = ctk.CTkFrame(master=self, fg_color=self.colors["alt_background"])
        tree_frame.pack(padx=10, fill="both", expand=True)
        
        columns = ("Projektnummer", "Projektname", "Beschreibung")
        self.project_treeview = ttk.Treeview(tree_frame, columns=columns, show="headings")
        apply_treeview_style(self.colors)
        
        self.update_idletasks()
        frame_width = self.winfo_width()
        
        num_columns = len(columns)
        if frame_width > 0:
            column_width = frame_width // num_columns
        else:
            column_width = 100
        
        for col in columns:
            self.project_treeview.heading(col, text=col)
            self.project_treeview.column(col, minwidth=50, width=column_width, stretch=True)
        
        self.project_treeview.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        # Scrollbar hinzufügen
        scrollbar = ctk.CTkScrollbar(
            tree_frame,
            command=self.project_treeview.yview,
            fg_color=self.colors["alt_background"],
            button_color=self.colors["background_light"],
        )
        self.project_treeview.configure(yscrollc=scrollbar.set)
        scrollbar.pack(side="right", fill="y", anchor="e")

        # Button zum Hinzufügen von Projekten
        add_project_button = ctk.CTkButton(
            master=self,
            text="Projekt hinzufügen",
            command=self.open_add_project_window,
            **self.styles["button"],
        )
        add_project_button.pack(pady=10, anchor="s")
        
         # Button zum Löschen von Projekten
        delete_project_button = ctk.CTkButton(
            master=self,
            text="Projekt Löchen",
            command=self.open_delete_project_window,
            **self.styles["button_error"],
        )
        delete_project_button.pack(pady=10, anchor="s")
        
        self.load_projects()
        
    def get_selected_project_number(self):
        """
        Gibt die Projektnummer und den Projektnamen des ausgewählten Eintrags zurück.

        Returns:
            tuple: Ein Tupel bestehend aus der Projektnummer und dem Projektnamen.
                   Gibt (None, None) zurück, wenn kein Projekt ausgewählt ist.

        Fehlerbehandlung:
        ------------------
        - Gibt None zurück, wenn kein Element im Treeview ausgewählt wurde.
        """
        try:
            selected_item = self.project_treeview.selection()[0]  # Die ID des ausgewählten Elements abrufen
            project_values = self.project_treeview.item(selected_item, 'values')  # Die Werte des ausgewählten Projekts abrufen
            if len(project_values) >= 2:
                return project_values[0], project_values[1]  # `project_number` und `project_name` zurückgeben
            return None, None
        except IndexError:
            return None, None  # Keine Auswahl
        
    def load_projects(self):
        """
        Lädt die Projekte aus der Datenbank und zeigt sie im Treeview an.

        Datenbankabfrage:
        -----------------
        - Ruft die Projektnummer, den Projektnamen und die Beschreibung aus der Tabelle `projects` ab.

        Fehlerbehandlung:
        ------------------
        - Zeigt eine Fehlermeldung an, falls die Datenbankverbindung oder Abfrage fehlschlägt.
        """
        for item in self.project_treeview.get_children():
            self.project_treeview.delete(item)
            
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("SELECT project_number, project_name, description FROM projects")
                projects = cursor.fetchall()
                for project in projects:
                    self.project_treeview.insert("", "end", values=(project[0], project[1], project[2]))
                    
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim Laden der Projekte {e}")
                
            finally:
                cursor.close()
                connection.close()
                
    def open_add_project_window(self):
        """
        Öffnet das Fenster zum Hinzufügen eines neuen Projekts.

        - Verwendet die Funktion `add_project`, um ein neues Projekt hinzuzufügen.
        - Aktualisiert die Projektliste nach erfolgreichem Hinzufügen.
        """
        add_project(self.master, self.load_projects)
        
    def open_delete_project_window(self):
        """
        Öffnet das Fenster zum Löschen eines ausgewählten Projekts.

        - Bestätigt die Aktion über eine Nachricht.
        - Verwendet die Funktion `delete_project`, um das Projekt aus der Datenbank zu entfernen.
        - Aktualisiert die Projektliste nach erfolgreichem Löschen.

        Fehlerbehandlung:
        ------------------
        - Zeigt eine Fehlermeldung an, wenn kein Projekt ausgewählt ist.
        """
        project_number = get_selected_project_number(self.project_treeview)
        if project_number is None:
            messagebox.showerror("Fehler", "Bitte wählen Sie ein Projekt aus")
            return
        
        confirmation = messagebox.askyesno("Bestätigung", "Sind Sie sicher, dass Sie dieses Projekt löschen möchten?")
        if confirmation:
            delete_project(project_number, self.load_projects)