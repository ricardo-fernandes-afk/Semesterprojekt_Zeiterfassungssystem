"""
Modul: Soll-Stunden speichern für TimeArch.

Dieses Modul speichert die Soll-Stunden für jede Phase eines Projekts in der Datenbank. Es aktualisiert
vorhandene Einträge oder fügt neue hinzu, falls diese noch nicht existieren.

Funktionen:
-----------
- save_soll_stunden(self): Speichert die Soll-Stunden für die Phasen eines Projekts in der Tabelle `project_sia_phases`.

Verwendung:
-----------
    from feature_save_soll_stunden import save_soll_stunden

    instance.save_soll_stunden()
"""

from db.db_connection import create_connection
from tkinter import messagebox

def save_soll_stunden(self):
    """
    Speichert die Soll-Stunden für jede Phase eines Projekts in der Tabelle `project_sia_phases`.

    Args:
        self: Die aktuelle Instanz, die Zugriff auf die `project_number` und `soll_stunden_entries` enthält.

    Datenbankintegration:
    ----------------------
    - Fügt Soll-Stunden für jede Phase des Projekts ein oder aktualisiert vorhandene Werte mithilfe der `ON CONFLICT`-Klausel.

    GUI-Integration:
    -----------------
    - Deaktiviert die Eingabefelder (`soll_stunden_entries`) nach erfolgreichem Speichern.
    - Zeigt eine Erfolgsmeldung an.

    Fehlerbehandlung:
    ------------------
    - Zeigt eine Fehlermeldung an, falls ein Fehler bei der Datenbankverbindung oder Abfrage auftritt.

    Beispiel:
    ---------
        instance.save_soll_stunden()
    """
    try:
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            for phase, entry in self.soll_stunden_entries.items():
                soll_stunden = entry.get()
                cursor.execute('''
                    INSERT INTO project_sia_phases (project_number, phase_name, soll_stunden)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (project_number, phase_name) DO UPDATE SET soll_stunden = EXCLUDED.soll_stunden;
                ''', (self.project_number, phase, soll_stunden))
            connection.commit()
            messagebox.showinfo("Erfolg", "Soll-Stunden erfolgreich gespeichert.")
            cursor.close()
            connection.close()
            self.toggle_entries(state="disabled")
            self.is_editable = False
    except Exception as e:
        messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten: {e}")