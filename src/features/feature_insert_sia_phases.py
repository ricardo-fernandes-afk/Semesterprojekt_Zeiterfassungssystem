"""
Modul: SIA-Phasen hinzufügen für TimeArch.

Dieses Modul fügt die SIA-Phasen mit ihren entsprechenden Phasennummern in die Tabelle `sia_phases` der Datenbank ein.
Es stellt sicher, dass keine Duplikate erstellt werden, falls die Phasen bereits existieren.

Funktionen:
-----------
- insert_sia_phases(cursor): Fügt die definierten SIA-Phasen zur Tabelle `sia_phases` hinzu.

Verwendung:
-----------
    from feature_insert_sia_phases import insert_sia_phases

    connection = create_connection()
    cursor = connection.cursor()
    insert_sia_phases(cursor)
    connection.commit()
"""

def insert_sia_phases(cursor): 
    """
    Fügt die SIA-Phasen zur Tabelle `sia_phases` hinzu.

    Details:
    --------
    - SIA-Phasen:
        - (2, "Vorstudien")
        - (3, "Projektierung")
        - (4, "Ausschreibung")
        - (5, "Realisierung")
    - Verwendet die ON CONFLICT-Klausel, um sicherzustellen, dass keine Duplikate erstellt werden.

    Args:
        cursor (psycopg2.extensions.cursor): Der Datenbank-Cursor, der für die Abfrage verwendet wird.

    Fehlerbehandlung:
    ------------------
    - Gibt eine Fehlermeldung aus, falls der Einfügevorgang fehlschlägt.

    Hinweis:
    --------
    - Diese Funktion setzt voraus, dass die Tabelle `sia_phases` bereits existiert.
    """
    sia_phases = [
        (2, "Vorstudien"),
        (3, "Projektierung"),
        (4, "Ausschreibung"),
        (5, "Realisierung")
    ]
    
    try:
            
        for phase_number, phase_name in sia_phases:
            cursor.execute('''
                INSERT INTO sia_phases (phase_number, phase_name)
                VALUES (%s, %s)
                ON CONFLICT (phase_number) DO NOTHING;
            ''', (phase_number, phase_name))
        print("SIA phases erfolgreich hinzugefügt!")
        
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")