from db_connection import create_connection
from feature_insert_sia_phases import insert_sia_phases

def setup_database():
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
        
        # Tabelle 'projects' erstellen
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                project_id SERIAL PRIMARY KEY,
                project_name VARCHAR(100) NOT NULL,
                description TEXT
            );
        ''')

        # Tabelle 'user_projects' erstellen, um Benutzer-Projekt-Zuordnungen zu speichern
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_projects (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(user_id),
                project_id INTEGER REFERENCES projects(project_id)
            );
        ''')
        
        # Tabelle 'sia_phases' erstellen, um die Struktur nach Norm aufzubauen
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS sia_phases (
                        phase_id SERIAL PRIMARY KEY,
                        phase_name VARCHAR(100) NOT NULL
            );
        ''')
        
        insert_sia_phases(cursor)

        # Tabelle 'time_entries' erstellen, um Arbeitszeiteinträge zu speichern
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS time_entries (
                entry_id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(user_id),
                project_id INTEGER REFERENCES projects(project_id),
                phase_id INTEGER REFERENCES sia_phases(phase_id),
                hours DECIMAL(5, 2),
                entry_date DATE DEFAULT CURRENT_DATE
            );
        ''')
        
        print("Tabellen erfolgreich erstellt")
        
        #Cursor und Verbindung schliessen
        cursor.close()
        connection.close()
        
if __name__ == "__main__":
    setup_database()
