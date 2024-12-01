from db.db_connection import create_connection

class EventHandlers:
    def __init__(self, admin_frame):
        self.admin_frame = admin_frame

    def on_project_double_click(self, event):
        # Überprüfen, ob ein Projekt ausgewählt wurde und die relevanten Daten abrufen
        project_number, project_name = self.admin_frame.project_frame.get_selected_project_number()
        
        if project_number:
            # Verbindung zur Datenbank herstellen, um zusätzliche Details abzurufen
            connection = create_connection()
            if connection:
                cursor = connection.cursor()
                try:
                    cursor.execute("SELECT project_number, project_name, description FROM projects WHERE project_number = %s", (project_number,))
                    project_details = cursor.fetchone()
                    if project_details:
                        project_number = project_details[0]
                        project_name = project_details[1]
                        description = project_details[2]
                        # Den `SelectedFrame` mit den abgerufenen Details öffnen und aktualisieren
                        self.admin_frame.open_selected_frame(project_number, project_name, description)
                except Exception as e:
                    print(f"Fehler beim Abrufen der Projektdetails: {e}")
                finally:
                    cursor.close()
                    connection.close()

    def on_user_double_click(self, event):
        # Überprüfen, ob ein Benutzer ausgewählt wurde und die relevanten Daten abrufen
        user_id, username = self.admin_frame.users_frame.get_selected_user()
        
        if not user_id:
            print("Fehler: Kein Benutzer ausgewählt.")
            return

        # Verbindung zur Datenbank herstellen, um zusätzliche Details abzurufen
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("SELECT username FROM users WHERE user_id = %s", (user_id,))
                user_details = cursor.fetchone()
                if user_details:
                    # Den `SelectedFrame` mit den abgerufenen Details öffnen und aktualisieren
                    self.admin_frame.open_selected_frame(None, user_details[0], None)
                else:
                    print("Fehler: Keine Benutzerdaten gefunden.")
            except Exception as e:
                print(f"Fehler beim Abrufen der Benutzerdetails: {e}")
            finally:
                cursor.close()
                connection.close()