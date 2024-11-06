from src.db_connection import create_connection

def insert_test_data():
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        
        
        # Testdaten einfügen
        cursor.execute("INSERT INTO users (username, password, role) VALUES ('ricardo', 'ricardo123', 'admin');")
        cursor.execute("INSERT INTO users (username, password, role) VALUES ('sven', 'sven123', 'user');")
        
        cursor.execute("INSERT INTO projects (project_name, description) VALUES ('Projekt A', '3 MFH');")
        cursor.execute("INSERT INTO projects (project_name, description) VALUES ('Projekt B', 'Umbau Büro');")
        
        connection.commit()
        print("Testdaten erfolgreich hinzugefügt")
        
        # Verbindung schliessen
        cursor.close()
        connection.close()
        
if __name__ == "__main__":
    insert_test_data()