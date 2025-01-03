"""
Datenbankverbindung für TimeArch.

Dieses Modul stellt die Verbindung zur PostgreSQL-Datenbank her, basierend auf den Konfigurationsparametern in `db_config.py`.

Module:
--------
- psycopg2: Zum Herstellen einer Verbindung zur PostgreSQL-Datenbank.
- db_config: Enthält die Konfigurationsparameter für die Verbindung.

Funktionen:
------------
- create_connection(): Erstellt und gibt eine Verbindung zur Datenbank zurück.

Verwendung:
------------
    from db_connection import create_connection

    connection = create_connection()
    if connection:
        print("Verbindung erfolgreich!")
        connection.close()
"""

import psycopg2
from db.db_config import DB_CONFIG

def create_connection():
    """
    Stellt eine Verbindung zur PostgreSQL-Datenbank her.

    Verwendet die Konfigurationsdetails aus `DB_CONFIG`, um eine Verbindung zu erstellen.

    Returns:
        connection (psycopg2.extensions.connection): Eine aktive Datenbankverbindung.
        None: Falls ein Fehler bei der Verbindung auftritt.

    Fehler:
        - Zeigt eine Fehlermeldung an, wenn die Verbindung nicht hergestellt werden kann.
    """
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        return connection
    except (Exception, psycopg2.Error) as error:
        print("Fehler bei der Verbindung:", error)
        return None