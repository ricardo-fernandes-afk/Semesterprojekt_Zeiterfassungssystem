import psycopg2
from db_config import DB_CONFIG

# Verbindung zur PostgreSQL-Datenbank herstellen

def create_connection(config):
    try:
        connection = psycopg2.connect(**config)
        return connection
    except (Exception, psycopg2.Error) as error:
        print("Fehler bei der Verbindung:", error)
        return None