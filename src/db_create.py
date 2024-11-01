import psycopg2
from db_config import DB_CONFIG

def create_database():
    try:
        # Verbindung zur Standard-Datenbank 'postgres' herstellen
        connection = psycopg2.connect(
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            database='postgres' # Standard-Datenbank verwenden
        )
        connection.autocommit = True    # Automatische Commit-Option aktivieren
        cursor = connection.cursor()
        
        # SQL-Befehl zum Erstellen der neuen Datenbank
        cursor.execute("CREATE DATABASE arc_zeiterfassung WITH ENCODING 'UTF8';")
        print("Datenbank 'arc-zeiterfassung' erfolgreich erstellt")
        
         # Cursor und Verbindung schließen
        cursor.close()
        connection.close()
        
    except (Exception, psycopg2.Error) as error:
        print("Fehler bei der Erstellung der Datenbank:", error)
        
if __name__ == "__main__":
    create_database()