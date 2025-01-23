"""
Modul: Projekterstellung für TimeArch.

Dieses Modul ermöglicht es Administratoren, neue Projekte zu erstellen und sie in die Datenbank einzufügen.
Die Benutzeroberfläche basiert auf CustomTkinter und integriert Funktionen zur Eingabe und Speicherung von Projektdetails.

Funktionen:
------------
- add_project(admin_window, refresh_callback):
    Öffnet ein neues Fenster zur Erstellung eines Projekts. Ermöglicht das Eingeben von Projektnummer, Projektnamen und Beschreibung.
    Fügt das Projekt in die Datenbank ein.
- save_project():
    Speichert das Projekt in der Datenbank. Validiert die Eingaben und zeigt Fehlermeldungen an, falls erforderlich.
    
Verwendung:
------------
    from feature_add_projects import add_project

    add_project(admin_window, refresh_callback)
"""

import customtkinter as ctk
from tkinter import messagebox
from gui.gui_appearance_color import appearance_color, get_default_styles
from db.db_connection import create_connection

def add_project(admin_window, refresh_callback):
    """
    Erstellt ein neues Projekt über ein Eingabefenster und fügt es in die Datenbank ein.

    Args:
        admin_window (ctk.CTk): Referenz zum Hauptfenster des Administrators.
        refresh_callback (function): Funktion, die nach der Projekterstellung aufgerufen wird, um die Ansicht zu aktualisieren.

    GUI-Komponenten:
    -----------------
    - Eingabefelder für Projektnummer, Projektnamen und Beschreibung.
    - Ein Button zum Speichern des Projekts.

    Datenbankintegration:
    ----------------------
    Fügt das Projekt in die Tabelle `projects` ein, sofern die Projektnummer und der Name angegeben sind.

    Hinweis:
    --------
    Zeigt eine Fehlermeldung, falls die Eingaben unvollständig sind oder ein Datenbankfehler auftritt.
    """
    colors = appearance_color()
    styles = get_default_styles()
    
    # Neues Fenster für die Projekterstellung
    project_window = ctk.CTkToplevel(admin_window)
    project_window.title("Neues Projekt erstellen")
    project_window.geometry("400x400")
    project_window.configure(fg_color=colors["background"])
    
    # Eingabefelder für den Projektnamen und die Beschreibung
    project_number_label = ctk.CTkLabel(project_window, text="Projektnummer", **styles["text"])
    project_number_label.pack(pady=10)
    project_number_entry = ctk.CTkEntry(project_window, **styles["entry"])
    project_number_entry.pack(pady=10)
    
    project_name_label = ctk.CTkLabel(project_window, text="Projektnamen", **styles["text"])
    project_name_label.pack(pady=10)
    project_name_entry = ctk.CTkEntry(project_window, **styles["entry"])
    project_name_entry.pack(pady=10)
    
    description_label = ctk.CTkLabel(project_window, text="Beschreibung", **styles["text"])
    description_label.pack(pady=10)
    description_entry = ctk.CTkEntry(project_window, **styles["entry"])
    description_entry.pack(pady=10)
    
    # Funktion, um das Projekt in die Datenbank einzufügen
    def save_project():
        """
        Speichert die Eingabedaten als neues Projekt in der Datenbank.

        Datenbankintegration:
        ----------------------
        - Validiert die Eingaben.
        - Fügt das Projekt in die Tabelle `projects` ein, falls keine Konflikte bestehen.

        Fehlerbehandlung:
        ------------------
        Zeigt Fehlermeldungen an, falls Eingaben unvollständig sind oder ein Datenbankfehler auftritt.
        """
        project_name = project_name_entry.get()
        description = description_entry.get()
        project_number = project_number_entry.get()
        
        if project_number and project_name:
            connection = create_connection()
            if connection:
                cursor = connection.cursor()
                try:
                    cursor.execute("INSERT INTO projects (project_number, project_name, description) VALUES (%s, %s, %s)", (project_number, project_name, description))
                    connection.commit()
                    messagebox.showinfo("Projekt erstellt", "Das Projekt wurde erfolgreich erstellt.")
                    refresh_callback()
                    project_window.destroy() # Fenster schließen, wenn das Projekt erfolgreich hinzugefügt wurde
                except:
                    messagebox.showerror("Fehler", "Ein Fehler ist aufgetreten. Bitte überprüfen!")
                finally:
                    cursor.close()
                    connection.close()
        else:
            messagebox.showerror("Fehler", "Bitte geben Sie einen Projektnamen ein.")

    # Button zum speichern des Projekts
    save_button = ctk.CTkButton(
        project_window,
        text="Speichern",
        command=save_project,
        **styles["button"],
        )
    save_button.pack(pady=20)
                    