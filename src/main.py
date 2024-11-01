from db_setup import setup_database
from db_connection import create_connection

def main():
    setup_database()    # Tabellen einrichten
    
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM users;")
        users = cursor.fetchall()
        for user in users:
            print(user)
            
        cursor.close()
        connection.close()

if __name__ == "__main__":
    main()