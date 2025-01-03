"""
Datenbankkonfigurationsdatei für TimeArch.

Dieses Modul enthält die Konfigurationsparameter für die Verbindung zur PostgreSQL-Datenbank.
Die Parameter umfassen Benutzername, Passwort, Host, Port und den Datenbanknamen.

Konfigurationsdetails:
- Benutzer: postgres
- Passwort: 1234
- Host: 127.0.0.1
- Port: 5432
- Datenbankname: arc_zeiterfassung

Hinweis:
- Die Konfigurationsparameter sind als Python-Dictionary definiert.
- Ändern Sie die Werte nach Bedarf entsprechend Ihrer Umgebung.

Beispiel:
--------
Verwendung der Konfiguration:
    from db_config import DB_CONFIG
    print(DB_CONFIG['host'])  # Gibt '127.0.0.1' aus
"""

DB_CONFIG = {
    'user': 'postgres',
    'password': '1234',
    'host': '127.0.0.1',
    'port': '5432',
    'database': 'arc_zeiterfassung'
}