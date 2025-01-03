"""
Modul: SIA-Phasen laden für TimeArch.

Dieses Modul lädt alle verfügbaren SIA-Phasen aus der Datenbank und gibt sie als Liste zurück.

Funktionen:
-----------
- load_sia_phases(): Lädt alle SIA-Phasen aus der Tabelle `sia_phases`.

Verwendung:
-----------
    from features_load_sia_phases import load_sia_phases

    sia_phases = load_sia_phases()
    print(sia_phases)
"""

from db.db_connection import create_connection

def load_sia_phases():
    """
    Lädt alle verfügbaren SIA-Phasen aus der Tabelle `sia_phases`.

    Returns:
        list: Eine Liste von Strings, wobei jeder String den Namen einer SIA-Phase darstellt.

    Datenbankabfrage:
    -----------------
    - Ruft die Spalte `phase_name` aus der Tabelle `sia_phases` ab.

    Fehlerbehandlung:
    ------------------
    - Gibt eine leere Liste zurück, falls die Verbindung zur Datenbank fehlschlägt oder keine Phasen vorhanden sind.

    Beispiel:
    ---------
        sia_phases = load_sia_phases()
        # Ergebnis: ["Vorstudien", "Projektierung", "Ausschreibung", "Realisierung"]
    """
    connection = create_connection()
    phases = []
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT phase_name FROM sia_phases")
        phases = cursor.fetchall()
        cursor.close()
        connection.close()
    return [phase[0] for phase in phases]  # Rückgabe einer Liste von Phasen