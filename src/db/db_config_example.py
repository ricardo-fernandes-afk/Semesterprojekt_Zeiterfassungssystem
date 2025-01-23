"""
Datenbankkonfigurationsdatei für TimeArch.

Dieses Modul enthält die Konfigurationsparameter für die Verbindung zur PostgreSQL-Datenbank.
Die Parameter umfassen Benutzername, Passwort, Host, Port und den Datenbanknamen.

Hinweis:
- Die Konfigurationsparameter sind als Python-Dictionary definiert.
- Ändern Sie die Werte nach Bedarf entsprechend Ihrer Umgebung.

Beispiel:
--------
Verwendung der Konfiguration:
    from db_config import DB_CONFIG
"""

DB_CONFIG = {
    'user': 'your_username',
    'password': 'your_password',
    'host': 'your_host',
    'port': 'your_port',
    'database': 'your_database'
}