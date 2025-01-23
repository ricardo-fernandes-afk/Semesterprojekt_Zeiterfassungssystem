"""
Modul: Soll-Stunden für ein Projekt laden in TimeArch.

Dieses Modul lädt die Soll-Stunden für jede Phase eines Projekts aus der Datenbank und aktualisiert die entsprechenden Eingabefelder in der Benutzeroberfläche.

Funktionen:
-----------
- load_soll_stunden(self): Lädt die Soll-Stunden für die Phasen eines Projekts aus der Tabelle `project_sia_phases`.

Verwendung:
-----------
    from feature_load_soll_stunden import load_soll_stunden

    instance.load_soll_stunden()
"""

from db.db_connection import create_connection
from tkinter import messagebox

def load_soll_stunden(self):
    """
    Lädt die Soll-Stunden für jede Phase eines Projekts aus der Datenbank und aktualisiert die Eingabefelder.

    Args:
        self: Die aktuelle Instanz, die Zugriff auf die `project_number` und `soll_stunden_entries` enthält.

    Datenbankabfrage:
    -----------------
    - Ruft die Phasennamen und deren Soll-Stunden aus der Tabelle `project_sia_phases` basierend auf der Projektnummer ab.

    GUI-Integration:
    -----------------
    - Aktualisiert die Eingabefelder (`soll_stunden_entries`) mit den abgerufenen Soll-Stunden.
    - Deaktiviert die Eingabefelder nach der Aktualisierung und setzt den Status `is_editable` auf False.

    Fehlerbehandlung:
    ------------------
    - Zeigt eine Fehlermeldung an, falls ein Fehler bei der Datenbankverbindung oder Abfrage auftritt.

    Beispiel:
    ---------
        instance.load_soll_stunden()
    """
    try:
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT phase_name, soll_stunden FROM project_sia_phases WHERE project_number = %s", (self.project_number,))
            results = cursor.fetchall()
            for phase_name, soll_stunden in results:
                if phase_name in self.soll_stunden_entries:
                    self.soll_stunden_entries[phase_name].delete(0, "end")
                    self.soll_stunden_entries[phase_name].insert(0, str(soll_stunden))
            cursor.close()
            connection.close()
            self.toggle_entries(state="disabled")
            self.is_editable = False
    except Exception as e:
        messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten: {e}")