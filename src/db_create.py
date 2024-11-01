from db_connection import create_connection
from db_config import DB_CONFIG_STANDARD

def create_database():
    connection = create_connection(DB_CONFIG_STANDARD)
    if connection:
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