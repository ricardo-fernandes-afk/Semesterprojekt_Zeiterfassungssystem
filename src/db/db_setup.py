"""
Datenbankeinrichtungsskript für TimeArch.

Dieses Modul erstellt alle notwendigen Tabellen und fügt Standardwerte in die PostgreSQL-Datenbank ein.
Es verwendet Funktionen aus `db_connection`, `feature_insert_sia_phases` und `feature_insert_admin`,
um sicherzustellen, dass die Struktur und Standardwerte gemäß den Anforderungen von TimeArch definiert sind.

Funktionen:
------------
- setup_database(): Erstellt alle Tabellen und fügt Standardwerte ein.

Verwendung:
------------
    python db_setup.py

Hinweis:
--------
- Stellen Sie sicher, dass die Verbindung zur PostgreSQL-Instanz hergestellt werden kann.
- Die Funktion überprüft, ob Tabellen bereits existieren, bevor sie erstellt werden.
"""

from db.db_connection import create_connection
from features.feature_insert_sia_phases import insert_sia_phases
from features.feature_insert_admin import insert_admin

def setup_database():
    """
    Erstellt alle notwendigen Tabellen und fügt Standardwerte in die PostgreSQL-Datenbank ein.

    Tabellen:
    ----------
    - `users`: Speichert Benutzerkonteninformationen.
    - `user_settings`: Speichert Einstellungen wie Arbeitszeit und Urlaub für Benutzer.
    - `projects`: Speichert Projekte mit Nummern und Beschreibungen.
    - `sia_phases`: Definiert Phasen gemäß SIA-Normen.
    - `user_projects`: Speichert Zuordnungen von Benutzern zu Projekten.
    - `project_sia_phases`: Speichert Sollstunden für spezifische Projektphasen.
    - `time_entries`: Speichert Zeiteinträge für Benutzer.

    Standardwerte:
    ---------------
    - Fügt das Projekt "Büro Intern" hinzu, falls es nicht existiert.
    - Fügt SIA-Phasen basierend auf `insert_sia_phases` ein.
    - Fügt den Standardadministrator basierend auf `insert_admin` ein.

    Returns:
        None

    Hinweis:
        - Die Verbindung wird automatisch geschlossen, nachdem die Tabellen erstellt wurden.
        - Gibt eine Erfolgsmeldung aus, wenn die Tabellen erfolgreich erstellt wurden.
    """
    connection = create_connection()
    if connection:
        connection.autocommit = True
        cursor = connection.cursor()

        #Tabelle 'users' erstellen
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                role VARCHAR(20) NOT NULL
            );
        ''')
        
        insert_admin(cursor)
        
        # Tabelle user_informations erstellen
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_settings (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(user_id),
            default_hours_per_day DECIMAL(4, 2) DEFAULT 8.5,
            employment_percentage INTEGER DEFAULT 100,
            vacation_hours DECIMAL(6,2) DEFAULT 212.50,
            start_date DATE
            );
        ''')
        
        # Tabelle 'projects' erstellen
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                project_id SERIAL PRIMARY KEY,
                project_number VARCHAR(50) UNIQUE NOT NULL,
                project_name VARCHAR(100) NOT NULL,
                description TEXT
            );
        ''')
        
        # Büro Intern Projekt einfügen
        cursor.execute('''
            INSERT INTO projects (project_number, project_name, description)
            VALUES ('0000', 'Büro Intern', 'Stunden für interne Büroaktivitäten')
            ON CONFLICT (project_number) DO NOTHING;
        ''')

        # Tabelle 'sia_phases' erstellen, um die Struktur nach Norm aufzubauen
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sia_phases (
                phase_id SERIAL PRIMARY KEY,
                phase_number INTEGER,
                phase_name VARCHAR(100) UNIQUE NOT NULL
            );
        ''')
        
        insert_sia_phases(cursor)
        
        # Tabelle 'user_projects' erstellen, um Benutzer-Projekt-Zuordnungen zu speichern
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_projects (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(user_id),
                project_number VARCHAR(50) REFERENCES projects(project_number)
            );
        ''')
        
        # Tabelle 'project_sia_phases' erstellen, um die Sollstunden Projektspezifisch zu speichern
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS project_sia_phases (
                project_number VARCHAR(50) REFERENCES projects(project_number),
                phase_name VARCHAR(100) REFERENCES sia_phases(phase_name),
                soll_stunden DECIMAL(10, 2),
                PRIMARY KEY (project_number, phase_name)
            );
        ''')

        # Tabelle 'time_entries' erstellen, um Arbeitszeiteinträge zu speichern
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS time_entries (
                entry_id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(user_id),
                project_number VARCHAR(50) REFERENCES projects(project_number),
                phase_id INTEGER REFERENCES sia_phases(phase_id),
                hours DECIMAL(5, 2),
                entry_date DATE DEFAULT CURRENT_DATE,
                activity VARCHAR(100) NOT NULL,
                note TEXT
            );
        ''')
        
        print("Tabellen erfolgreich erstellt")
        
        #Cursor und Verbindung schliessen
        cursor.close()
        connection.close()
        
if __name__ == "__main__":
    setup_database()
