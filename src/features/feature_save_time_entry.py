from db.db_connection import create_connection

def save_hours(user_id, project_number, phase_id, hours, entry_date, activity, note=None):
    """Speichert die Stunden in der Datenbank."""
    if not all([user_id, project_number, phase_id, hours, entry_date, activity]):
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
