from db.db_connection import create_connection

def load_project_users(project_number):
    # Verbindet sich mit der Datenbank und lädt die Benutzer, die einem bestimmten Projekt zugeordnet sind
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