"""
Modul: Projektbenutzer laden für TimeArch.

Dieses Modul lädt alle Benutzer, die einem bestimmten Projekt zugeordnet sind, aus der Datenbank.

Funktionen:
-----------
- load_project_users(project_number): Lädt die Benutzer eines Projekts aus der Datenbank.

Verwendung:
-----------
    from feature_load_project_users import load_project_users

    project_users = load_project_users(project_number)
    for user_id, username in project_users:
        print(f"Benutzer-ID: {user_id}, Benutzername: {username}")
"""

from db.db_connection import create_connection

def load_project_users(project_number):
    """
    Lädt die Benutzer, die einem bestimmten Projekt zugeordnet sind.

    Args:
        project_number (str): Die Projektnummer, für die die Benutzer geladen werden sollen.

    Returns:
        list: Eine Liste von Tupeln, wobei jedes Tupel die Benutzer-ID und den Benutzernamen enthält.

    Datenbankabfrage:
    -----------------
    - Ruft Benutzerinformationen (user_id und username) aus der Tabelle `user_projects` ab,
      die mit der Tabelle `users` verknüpft ist.

    Fehlerbehandlung:
    ------------------
    - Gibt eine leere Liste zurück, falls ein Fehler bei der Abfrage oder der Verbindung auftritt.

    Beispiel:
    ---------
        project_users = load_project_users("P123")
        # Ergebnis: [(1, "user1"), (2, "user2")]
    """
    try:
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT u.user_id, u.username 
                FROM user_projects up
                JOIN users u ON up.user_id = u.user_id
                WHERE up.project_number = %s
            """, (project_number,))
            results = cursor.fetchall()
            cursor.close()
            connection.close()
            return results
    except Exception as e:
        print(f"Fehler beim Laden der Benutzer für das Projekt: {e}")
        return []