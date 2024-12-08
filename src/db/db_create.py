from db.db_connection import create_connection

def create_database():
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