import psycopg2
from db_config import DB_CONFIG

# Verbindung zur PostgreSQL-Datenbank herstellen

def create_connection():
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        return connection
    except (Exception, psycopg2.Error) as error:
        print("Fehler bei der Verbindung:", error)
        return None