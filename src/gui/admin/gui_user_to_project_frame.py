"""
Modul: Benutzer einem Projekt zuweisen in TimeArch.

Dieses Modul stellt die grafische Benutzeroberfläche bereit, um Benutzer einem Projekt zuzuweisen oder sie daraus zu entfernen. Es umfasst Funktionen zum Laden der Benutzerliste, Zuweisen von Benutzern zu einem Projekt und Entfernen von Benutzern aus einem Projekt.

Klassen:
--------
- UserToProjectFrame: Hauptklasse für die Verwaltung der Benutzer eines Projekts.

Methoden:
---------
- __init__(self, master, project_number): Initialisiert das Frame mit dem Projektkontext.
- create_widgets(self): Erstellt die Widgets zur Benutzerzuweisung und -verwaltung.
- load_users(self): Lädt die Liste aller verfügbaren Benutzer aus der Datenbank.
- load_project_users(self): Lädt die Liste der Benutzer, die einem bestimmten Projekt zugeordnet sind.
- update_users_treeview(self): Aktualisiert die Anzeige der Benutzer im Projekt in der Treeview.
- assign_user_to_project(self): Weist den ausgewählten Benutzer dem Projekt zu.
- delete_user_from_project(self): Entfernt den ausgewählten Benutzer aus dem Projekt.

Verwendung:
-----------
    from gui_user_to_project_frame import UserToProjectFrame

    frame = UserToProjectFrame(master, project_number="P123")
    frame.pack()
"""

import customtkinter as ctk
from db.db_connection import create_connection
from tkinter import messagebox, ttk
from features.feature_load_users import load_users
from features.feature_load_project_users import load_project_users
from gui.gui_appearance_color import appearance_color, get_default_styles, apply_treeview_style

class UserToProjectFrame(ctk.CTkFrame):
    """
    Eine Klasse, die die Benutzer eines Projekts verwaltet.

    Ermöglicht das Hinzufügen und Entfernen von Benutzern sowie die Anzeige der aktuell zugeordneten Benutzer.
    """
    def __init__(self, master, project_number):
        """
        Initialisiert den Frame für die Benutzerzuweisung.

        Args:
            master (ctk.CTk): Das übergeordnete Fenster.
            project_number (str): Die Projektnummer, für die die Benutzer verwaltet werden sollen.
        """
        self.colors = appearance_color()
        self.styles = get_default_styles()
        
        super().__init__(master, corner_radius=10, fg_color=self.colors["alt_background"])
        self.project_number = project_number
        self.available_users = []
        self.project_users = []
        self.create_widgets()
        self.load_users()
        self.load_project_users()

    def create_widgets(self):
        """
        Erstellt die Widgets für die Benutzerverwaltung.

        - Fügt Dropdowns für die Benutzerliste hinzu.
        - Erstellt Buttons für das Zuweisen und Entfernen von Benutzern.
        - Fügt ein Treeview hinzu, um die Benutzer im Projekt anzuzeigen.
        """
        # Label für User-Zuweisung
        self.label = ctk.CTkLabel(self, text="Benutzer zuweisen", **self.styles["subtitle"])
        self.label.pack(pady=10, padx=10)
        
        # User-Auswahl Dropdown
        self.user_dropdown = ctk.CTkComboBox(self, **self.styles["combobox"])
        self.user_dropdown.pack(padx=10, fill="x", expand=False)
        
        # Zuweisen-Button
        self.assign_button = ctk.CTkButton(
            self,
            text="Benutzer zuweisen",
            command=self.assign_user_to_project,
            **self.styles["button"]
        )
        self.assign_button.pack(padx=10, pady=10)
        
        # Treeview für die Liste der Benutzer im Projekt
        treeview_frame = ctk.CTkFrame(self, fg_color=self.colors["alt_background"])
        treeview_frame.pack(padx=10, fill="both", expand=True)
        
        columns = ("Benutzer-ID", "Benutzername")
        self.users_treeview = ttk.Treeview(treeview_frame, columns=columns, show="headings", height=5)
        apply_treeview_style(self.colors)
        
        for col in columns:
            self.users_treeview.heading(col, text=col)
            self.users_treeview.column(col, width=100)
        self.users_treeview.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        # Scrollbar hinzufügen
        scrollbar = ctk.CTkScrollbar(
            treeview_frame,
            command=self.users_treeview.yview,
            height=5,
            fg_color=self.colors["alt_background"],
            button_color=self.colors["background_light"]
        )
        self.users_treeview.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y", anchor="e")
        
        # Löschen-Button
        self.delete_button = ctk.CTkButton(
            self,
            text="Benutzer entfernen",
            command=self.delete_user_from_project,
            **self.styles["button_error"]
        )
        self.delete_button.pack(pady=10, padx=10)

    def load_users(self):
        """
        Lädt die Liste aller verfügbaren Benutzer aus der Datenbank.

        - Verwendet die Funktion `load_users` aus den Features.
        - Füllt das Dropdown-Menü mit den abgerufenen Benutzern.

        Fehlerbehandlung:
        ------------------
        - Zeigt eine Fehlermeldung an, falls die Datenbankabfrage fehlschlägt.
        """
        # Verwende die ausgelagerte Funktion `load_users`
        users = load_users()
        self.available_users = [f"{user[0]} - {user[1]}" for user in users]
        self.user_dropdown.configure(values=self.available_users)
        
    def load_project_users(self):
        """
        Lädt die Liste der Benutzer, die dem aktuellen Projekt zugeordnet sind.

        - Verwendet die Funktion `load_project_users` aus den Features.
        - Aktualisiert die Treeview mit den Benutzerdaten.

        Fehlerbehandlung:
        ------------------
        - Zeigt eine Fehlermeldung an, falls die Datenbankabfrage fehlschlägt.
        """
        # Benutzer, die bereits dem Projekt zugeordnet sind, aus der Datenbank laden
        users = load_project_users(self.project_number)
        self.project_users = users
        self.update_users_treeview()
    
    def update_users_treeview(self):
        """
        Aktualisiert die Treeview mit den Benutzern, die dem Projekt zugeordnet sind.

        - Löscht alle bestehenden Einträge in der Treeview.
        - Fügt die aktuelle Liste der Projektbenutzer hinzu.
        """
        # Die Liste der Benutzer im Projekt aktualisieren
        for item in self.users_treeview.get_children():
            self.users_treeview.delete(item)
        for user in self.project_users:
            self.users_treeview.insert("", "end", values=(user[0], user[1]))        
    
    def assign_user_to_project(self):
        """
        Weist den ausgewählten Benutzer dem Projekt zu.

        - Führt eine Datenbankabfrage durch, um die Zuweisung zu speichern.
        - Aktualisiert die Treeview nach der erfolgreichen Zuweisung.

        Fehlerbehandlung:
        ------------------
        - Zeigt eine Fehlermeldung an, falls die Zuweisung fehlschlägt.
        """
        # Weisen Sie den ausgewählten Benutzer dem aktuell ausgewählten Projekt zu
        user_selection = self.user_dropdown.get()
        if not user_selection:
            messagebox.showerror("Fehler", "Bitte wählen Sie einen Benutzer aus")
            return
        
        user_id = int(user_selection.split(" - ")[0])
        
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute(
                    "INSERT INTO user_projects (user_id, project_number) VALUES (%s, %s)",
                    (user_id, self.project_number)
                )
                connection.commit()
                messagebox.showinfo("Erfolg", "Benutzer erfolgreich zugewiesen")
                self.load_project_users()  # Aktualisiere die Liste der Projekt-Benutzer
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler bei der Zuweisung des Benutzers: {e}")
            finally:
                cursor.close()
                connection.close()
    
    def delete_user_from_project(self):
        """
        Entfernt den ausgewählten Benutzer aus dem Projekt.

        - Führt eine Datenbankabfrage durch, um die Zuweisung zu löschen.
        - Aktualisiert die Treeview nach dem erfolgreichen Entfernen.

        Fehlerbehandlung:
        ------------------
        - Zeigt eine Fehlermeldung an, falls das Entfernen fehlschlägt.
        """
        # Benutzer aus Projekt entfernen
        selected_item = self.users_treeview.selection()
        if not selected_item:
            messagebox.showerror("Fehler", "Bitte wählen Sie einen Benutzer aus der Liste aus")
            return

        user_id = self.users_treeview.item(selected_item, "values")[0]
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute(
                    "DELETE FROM user_projects WHERE user_id = %s AND project_number = %s",
                    (user_id, self.project_number)
                )
                connection.commit()
                messagebox.showinfo("Erfolg", "Benutzer erfolgreich entfernt")
                self.load_project_users()  # Aktualisiere die Liste der Projekt-Benutzer
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim Entfernen des Benutzers: {e}")
            finally:
                cursor.close()
                connection.close()
