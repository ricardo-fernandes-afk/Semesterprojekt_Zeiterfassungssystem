"""
Modul: Zeitbuchung speichern für TimeArch.

Dieses Modul speichert Zeiteinträge für Benutzer in der Datenbank. Es erfasst Details wie Stunden,
Projektzuordnung, Phasen, Tätigkeiten und Notizen.

Funktionen:
-----------
- save_hours(user_id, project_number, phase_id, hours, entry_date, activity, note=None): Speichert die Stunden in der Tabelle `time_entries`.

Verwendung:
-----------
    from feature_save_time_entry import save_hours

    result = save_hours(user_id, project_number, phase_id, hours, entry_date, activity, note)
    if result:
        print("Stunden erfolgreich gespeichert.")
    else:
        print("Fehler beim Speichern der Stunden.")
"""

from db.db_connection import create_connection

def save_hours(user_id, project_number, phase_id, hours, entry_date, activity, note=None):
    """
    Speichert die Stunden in der Tabelle `time_entries`.

    Args:
        user_id (int): Die Benutzer-ID, die die Stunden eingibt.
        project_number (str): Die Projektnummer, der die Stunden zugeordnet sind.
        phase_id (int): Die ID der Phase, der die Stunden zugeordnet sind.
        hours (float): Die Anzahl der Stunden, die eingegeben werden.
        entry_date (str): Das Datum der Eingabe im Format YYYY-MM-DD.
        activity (str): Die Aktivität, für die die Stunden gebucht werden.
        note (str, optional): Zusätzliche Notizen zu den Stunden. Standard ist None.

    Returns:
        bool: True, wenn die Stunden erfolgreich gespeichert wurden, andernfalls False.

    Datenbankintegration:
    ----------------------
    - Fügt einen neuen Eintrag in die Tabelle `time_entries` ein.

    Fehlerbehandlung:
    ------------------
    - Gibt False zurück, falls Eingabeinformationen unvollständig sind oder ein Fehler bei der Datenbankverbindung auftritt.

    Beispiel:
    ---------
        result = save_hours(1, "P123", 2, 8.0, "2025-01-01", "Planung", "Details zur Aufgabe")
        if result:
            print("Stunden erfolgreich gespeichert.")
    """
    if not all([user_id, project_number, hours, entry_date, activity]):
        print("Fehler: Unvollständige Informationen zum Speichern der Stunden.")
        return False

    try:
        connection = create_connection()
        cursor = connection.cursor()
        query = """
        INSERT INTO time_entries (user_id, project_number, phase_id, hours, entry_date, activity, note)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query,(user_id, project_number, phase_id, hours, entry_date, activity, note))
        connection.commit()
        print(f"Stunden erfolgreich gespeichert: {hours} Stunden für {entry_date}, Tätigkeit: {activity}")
        return True
    except Exception as e:
        print(f"Fehler beim Speichern der Stunden: {e}")
        return False
    finally:
        if connection:
            cursor.close()
            connection.close()
