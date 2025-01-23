"""
Modul: Admin-Benutzer hinzufügen für TimeArch.

Dieses Modul fügt einen Standard-Admin-Benutzer zur Datenbank hinzu. Es wird verwendet, um sicherzustellen,
dass immer mindestens ein Administrator vorhanden ist, falls keine anderen Benutzer existieren.

Funktionen:
-----------
- insert_admin(cursor): Fügt den Standard-Admin-Benutzer in die Tabelle `users` ein.

Verwendung:
-----------
    from feature_insert_admin import insert_admin

    connection = create_connection()
    cursor = connection.cursor()
    insert_admin(cursor)
    connection.commit()
"""

def insert_admin(cursor): 
    """
    Fügt einen Standard-Admin-Benutzer zur Tabelle `users` hinzu.

    Details:
    --------
    - Standardbenutzer:
        - Benutzername: "adm"
        - Passwort: "123"
        - Rolle: "admin"
    - Verwendet die ON CONFLICT-Klausel, um sicherzustellen, dass keine Duplikate erstellt werden.

    Args:
        cursor (psycopg2.extensions.cursor): Der Datenbank-Cursor, der für die Abfrage verwendet wird.

    Fehlerbehandlung:
    ------------------
    - Gibt eine Fehlermeldung aus, falls der Einfügevorgang fehlschlägt.

    Hinweis:
    --------
    - Diese Funktion setzt voraus, dass die Tabelle `users` bereits existiert.
    """
    start_admin = [("adm", 123, "admin")]
    
    try:
            
        for username, password, role in start_admin:
            cursor.execute('''
                INSERT INTO users (username, password, role)
                VALUES (%s, %s, %s)
                ON CONFLICT (username) DO NOTHING;
            ''', (username, password, role))
        print("Start Admin hinzugefügt")
        
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")