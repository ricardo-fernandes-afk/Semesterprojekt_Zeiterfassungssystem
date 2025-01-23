"""
Modul: Benutzer laden für TimeArch.

Dieses Modul lädt alle Benutzer aus der Datenbank und gibt sie als Liste zurück.

Funktionen:
-----------
- load_users(): Lädt Benutzerinformationen (ID und Benutzername) aus der Tabelle `users`.

Verwendung:
-----------
    from feature_load_users import load_users

    users = load_users()
    for user_id, username in users:
        print(f"Benutzer-ID: {user_id}, Benutzername: {username}")
"""

from db.db_connection import create_connection
from tkinter import messagebox

def load_users():
    """
    Lädt alle Benutzerinformationen aus der Tabelle `users`.

    Returns:
        list: Eine Liste von Tupeln, wobei jedes Tupel die Benutzer-ID und den Benutzernamen enthält.

    Datenbankabfrage:
    -----------------
    - Ruft die Spalten `user_id` und `username` aus der Tabelle `users` ab.

    Fehlerbehandlung:
    ------------------
    - Zeigt eine Fehlermeldung an, falls ein Fehler bei der Abfrage oder der Verbindung auftritt.

    Beispiel:
    ---------
        users = load_users()
        # Ergebnis: [(1, "user1"), (2, "user2")]
    """
    users = []
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT user_id, username FROM users")
            users = cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Laden der Benutzer: {e}")
        finally:
            cursor.close()
            connection.close()
    
    return users
