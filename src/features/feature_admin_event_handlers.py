"""
Event-Handler-Modul für TimeArch-Admin-Interface.

Dieses Modul enthält die Ereignis-Handler-Klasse `EventHandlers`, die für die Verarbeitung
von Benutzerinteraktionen im Admin-Interface verantwortlich ist. Es behandelt Ereignisse wie
Doppelklicks auf Benutzer- und Projektlisten und ruft dabei relevante Daten aus der Datenbank ab.

Klassen:
--------
- EventHandlers: Enthält Methoden zur Verarbeitung von Benutzer- und Projektinteraktionen.

Funktionen:
-----------
- on_project_double_click(event): Verarbeitet Doppelklicks auf ein Projekt in der Projektliste.
- on_user_double_click(event): Verarbeitet Doppelklicks auf einen Benutzer in der Benutzerliste.

Verwendung:
-----------
    from feature_admin_event_handlers import EventHandlers

    event_handler = EventHandlers(admin_frame)
    admin_frame.project_frame.bind("<Double-1>", event_handler.on_project_double_click)
"""

from db.db_connection import create_connection

class EventHandlers:
    """
    Eine Klasse für Ereignis-Handler im Admin-Interface.

    Diese Klasse verarbeitet Interaktionen wie Doppelklicks auf Projekte und Benutzer und
    aktualisiert entsprechend den Inhalt des `SelectedFrame`.
    """
    def __init__(self, admin_frame):
        """
        Initialisiert den EventHandler mit einer Referenz auf den Admin-Frame.

        Args:
            admin_frame: Das Admin-Interface, das die Frames und Datenstrukturen enthält.
        """
        self.admin_frame = admin_frame

    def on_project_double_click(self, event):
        """
        Verarbeitet Doppelklicks auf ein Projekt in der Projektliste.

        - Ruft die Projektdetails (Nummer, Name, Beschreibung) aus der Datenbank ab.
        - Aktualisiert den `SelectedFrame` mit den abgerufenen Daten.

        Args:
            event: Das Ereignisobjekt, das den Doppelklick beschreibt.

        Fehlerbehandlung:
        -----------------
        - Gibt Fehlermeldungen aus, wenn keine Projektdetails gefunden werden.
        """
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
        """
        Verarbeitet Doppelklicks auf einen Benutzer in der Benutzerliste.

        - Ruft die Benutzerdetails (ID, Name) aus der Datenbank ab.
        - Aktualisiert den `SelectedFrame` mit den abgerufenen Daten.

        Args:
            event: Das Ereignisobjekt, das den Doppelklick beschreibt.

        Fehlerbehandlung:
        -----------------
        - Gibt Fehlermeldungen aus, wenn keine Benutzerdetails gefunden werden.
        """
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
                    self.admin_frame.selected_frame.update_user_details(user_id, user_details[0])
                else:
                    print("Fehler: Keine Benutzerdaten gefunden.")
            except Exception as e:
                print(f"Fehler beim Abrufen der Benutzerdetails: {e}")
            finally:
                cursor.close()
                connection.close()