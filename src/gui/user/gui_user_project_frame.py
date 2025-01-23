"""
Modul: Benutzer-Projekt-Frame für TimeArch.

Dieses Modul bietet eine grafische Benutzeroberfläche, die die Projekte eines Benutzers anzeigt. Es verwendet ein Treeview-Widget zur Darstellung von Projektnummer, Projektname und Beschreibung.

Klassen:
--------
- UserProjectFrame: Hauptklasse zur Anzeige der Projekte eines Benutzers.

Methoden:
---------
- __init__(self, master, username): Initialisiert den Frame mit dem Benutzernamen und erstellt die Widgets.
- load_user_projects(self): Lädt die Projekte des Benutzers aus der Datenbank und füllt das Treeview.

Verwendung:
-----------
    from gui_user_project_frame import UserProjectFrame

    frame = UserProjectFrame(master, username="John Doe")
    frame.pack()
"""

import customtkinter as ctk
from tkinter import ttk, messagebox
from db.db_connection import create_connection
from gui.gui_appearance_color import appearance_color, get_default_styles, apply_treeview_style

class UserProjectFrame(ctk.CTkFrame):
    """
    Eine Klasse zur Anzeige der Projekte eines Benutzers.

    Funktionen:
    - Projekte in einem Treeview anzeigen
    - Datenbankverbindung zum Laden der Projekte nutzen
    """
    def __init__(self, master, username):
        """
        Initialisiert das Benutzer-Projekt-Frame.

        Args:
            master (ctk.CTk): Das übergeordnete Fenster.
            username (str): Der Benutzername des aktuellen Benutzers.
        """
        self.colors = appearance_color()
        self.styles = get_default_styles()
        apply_treeview_style(self.colors)
        
        super().__init__(master, corner_radius=10, fg_color=self.colors["background"])
        self.username = username

        # Label für Projekte
        project_label = ctk.CTkLabel(master=self, text="Meine Projekte", **self.styles["title"])
        project_label.pack(pady=10, anchor="n")

        # Projektliste
        tree_frame = ctk.CTkFrame(master=self, fg_color=self.colors["alt_background"])
        tree_frame.pack(padx=10, pady=(0,10), fill="both", expand=True)
        
        columns = ("Projektnummer", "Projektname", "Beschreibung")
        self.project_treeview = ttk.Treeview(tree_frame, columns=columns, show="headings")
        
        for col in columns:
            self.project_treeview.heading(col, text=col)
            self.project_treeview.column(col, width=200, stretch=True)
        
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

        # Projekte laden
        self.load_user_projects()
        

    def load_user_projects(self):
        """
        Lädt die Projekte des Benutzers aus der Datenbank und füllt das Treeview.

        - Verwendet den Benutzernamen, um die mit dem Benutzer verknüpften Projekte zu laden.
        - Fügt die Projektdaten in das Treeview-Widget ein.

        Fehlerbehandlung:
        ------------------
        - Zeigt eine Fehlermeldung an, falls die Datenbankabfrage fehlschlägt.
        """
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                query = """
                SELECT p.project_number, p.project_name, p.description
                FROM projects p
                JOIN user_projects up ON p.project_number = up.project_number
                JOIN users u ON up.user_id = u.user_id
                WHERE u.username = %s
                """
                cursor.execute(query, (self.username,))
                projects = cursor.fetchall()
                
                projects.sort(key=lambda x: x[0])
                
                for project in projects:
                    self.project_treeview.insert("", "end", values=project)
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim Laden der Projekte: {e}")
            finally:
                cursor.close()
                connection.close()
