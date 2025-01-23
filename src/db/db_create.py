"""
Datenbankerstellungsskript für TimeArch.

Dieses Modul erstellt die PostgreSQL-Datenbank `arc_zeiterfassung`, falls sie noch nicht existiert.
Das Skript verwendet die Verbindung aus `db_connection.py`.

Funktionen:
------------
- create_database(): Erstellt die Datenbank `arc_zeiterfassung`.

Verwendung:
------------
    python db_create.py

Hinweis:
--------
- Stellen Sie sicher, dass die Verbindung zur PostgreSQL-Instanz hergestellt werden kann und die notwendigen Berechtigungen vorhanden sind, um eine neue Datenbank zu erstellen.
"""

from db.db_connection import create_connection

def create_database():
    """
    Erstellt die PostgreSQL-Datenbank `arc_zeiterfassung`.

    Verwendet die Verbindung aus `db_connection.py`, aktiviert den Autocommit-Modus,
    und führt den SQL-Befehl zum Erstellen der Datenbank aus.

    Returns:
        None

    Hinweis:
        - Die Verbindung wird automatisch geschlossen, nachdem die Datenbank erstellt wurde.
        - Gibt eine Erfolgsmeldung aus, wenn die Datenbank erfolgreich erstellt wurde.
    """
    connection = create_connection()
    if connection:
        connection.autocommit = True    # Automatische Commit-Option aktivieren
        cursor = connection.cursor()
        
        # SQL-Befehl zum Erstellen der neuen Datenbank
        cursor.execute("CREATE DATABASE arc_zeiterfassung WITH ENCODING 'UTF8';")
        print("Datenbank 'arc-zeiterfassung' erfolgreich erstellt")
        
         # Cursor und Verbindung schließen
        cursor.close()
        connection.close()
        
if __name__ == "__main__":
    create_database()