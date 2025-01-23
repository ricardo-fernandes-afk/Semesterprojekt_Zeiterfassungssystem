"""
Modul: Projektlöschung für TimeArch.

Dieses Modul ermöglicht es Administratoren, Projekte aus der Datenbank zu löschen.
Es enthält Funktionen zum Abrufen der ausgewählten Projektnummer und zum Löschen eines Projekts.

Funktionen:
-----------
- get_selected_project_number(treeview): Gibt die Projektnummer des ausgewählten Eintrags in einem Treeview zurück.
- delete_project(project_number, refresh_callback): Löscht ein Projekt anhand seiner Projektnummer.

Verwendung:
-----------
    from feature_delete_project import get_selected_project_number, delete_project

    project_number = get_selected_project_number(treeview)
    delete_project(project_number, refresh_callback)
"""
import customtkinter as ctk
from tkinter import ttk
from tkinter import messagebox
from db.db_connection import create_connection

def get_selected_project_number(treeview):
    """
    Gibt die Projektnummer des ausgewählten Eintrags in einem Treeview zurück.

    Args:
        treeview (ttk.Treeview): Das Treeview-Widget, das die Projektdaten enthält.

    Returns:
        str: Die Projektnummer des ausgewählten Eintrags, falls vorhanden.
        None: Falls kein Eintrag ausgewählt wurde oder keine Projektnummer gefunden wurde.

    Hinweis:
    --------
    - Überprüft, ob ein Eintrag ausgewählt wurde.
    - Extrahiert die Werte aus der Auswahl und gibt die Projektnummer zurück.
    """
    selected_item = treeview.selection()    # Liefert die ID des ausgewählten Treeview-Eintrags
    if not selected_item:
        return None
    
    # Hole die Daten des ausgewählten Eintrags
    project_data = treeview.item(selected_item)
    project_values = project_data.get("values")
    
    # Sicherstellen, dass wir tatsächlich Werte erhalten und die Benutzer-ID korrekt extrahieren
    if project_values and len(project_values) > 0:
        return project_values[0]
    return None      

def delete_project(project_number, refresh_callback):
    """
    Löscht ein Projekt anhand seiner Projektnummer aus der Datenbank.

    Args:
        project_number (str): Die Projektnummer des zu löschenden Projekts.
        refresh_callback (function): Eine Callback-Funktion, die nach dem Löschen aufgerufen wird, um die Ansicht zu aktualisieren.

    Hinweis:
    --------
    - Verhindert das Löschen des Projekts "Büro Intern" (`project_number = '0000'`).
    - Verwendet eine Datenbankverbindung zum Ausführen der Löschanweisung.
    - Zeigt eine Fehlermeldung an, falls ein Fehler auftritt.
    """
    # Verhindern, dass das Büro Intern Projekt gelöscht wird
    if project_number == "0000":
        messagebox.showerror("Fehler", "Das Büro Intern Projekt kann nicht gelöscht werden.")
        return
    
    connection = create_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM projects WHERE project_number = %s", (project_number,))
                connection.commit()
                messagebox.showinfo("Erfolg", "Projekt erfolgreich gelöscht.")
                refresh_callback()
        except Exception as e:
            messagebox.showerror("Fehler", str(e))
        finally:
            connection.close()