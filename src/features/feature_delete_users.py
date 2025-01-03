"""
Modul: Benutzerlöschung für TimeArch.

Dieses Modul ermöglicht es Administratoren, Benutzer aus der Datenbank zu löschen.
Es enthält Funktionen zum Abrufen der ausgewählten Benutzer-ID und zum Löschen eines Benutzers.

Funktionen:
-----------
- get_selected_user_id(treeview): Gibt die Benutzer-ID des ausgewählten Eintrags in einem Treeview zurück.
- delete_user(user_id, refresh_callback): Löscht einen Benutzer anhand seiner Benutzer-ID.

Verwendung:
-----------
    from feature_delete_users import get_selected_user_id, delete_user

    user_id = get_selected_user_id(treeview)
    delete_user(user_id, refresh_callback)
"""

import customtkinter as ctk
from tkinter import ttk
from tkinter import messagebox
from db.db_connection import create_connection

def get_selected_user_id(treeview):
    """
    Gibt die Benutzer-ID des ausgewählten Eintrags in einem Treeview zurück.

    Args:
        treeview (ttk.Treeview): Der Treeview, der die Benutzerliste darstellt.

    Returns:
        str: Die Benutzer-ID des ausgewählten Eintrags, oder None, wenn kein Eintrag ausgewählt wurde.

    Hinweis:
        - Überprüft, ob ein Eintrag ausgewählt wurde.
        - Extrahiert die Benutzer-ID aus den Wertefeldern des ausgewählten Treeview-Eintrags.
    """
    selected_item = treeview.selection()    # Liefert die ID des ausgewählten Treeview-Eintrags
    if not selected_item:
        return None
    
    # Hole die Daten des ausgewählten Eintrags
    user_data = treeview.item(selected_item)
    user_values = user_data.get("values")
    
    # Sicherstellen, dass wir tatsächlich Werte erhalten und die Benutzer-ID korrekt extrahieren
    if user_values and len(user_values) > 0:
        return user_values[0]
    return None      

def delete_user(user_id, refresh_callback):
    """
    Löscht einen Benutzer anhand seiner Benutzer-ID aus der Datenbank.

    Args:
        user_id (str): Die Benutzer-ID des zu löschenden Benutzers.
        refresh_callback (function): Funktion, die nach der Löschung aufgerufen wird, um die Ansicht zu aktualisieren.

    Datenbankintegration:
    ----------------------
    - Verwendet die Benutzer-ID, um den Benutzer aus der Tabelle `users` zu entfernen.

    Fehlerbehandlung:
    ------------------
    - Zeigt Fehlermeldungen an, falls ein Datenbankfehler auftritt.

    Hinweis:
        - Verbindung wird nach Abschluss der Operation geschlossen.
        - Zeigt eine Erfolgsmeldung an, wenn der Benutzer erfolgreich gelöscht wurde.
    """
    connection = create_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
                connection.commit()
                messagebox.showinfo("Erfolg", "Benutzer erfolgreich gelöscht.")
                refresh_callback()
        except Exception as e:
            messagebox.showerror("Fehler", str(e))
        finally:
            connection.close()