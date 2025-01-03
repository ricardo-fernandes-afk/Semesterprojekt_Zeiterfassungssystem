"""
Modul: Benutzer-Ereignis-Handler für TimeArch.

Dieses Modul enthält Ereignis-Handler für Benutzerinteraktionen mit Projekten im User-Interface. Es ermöglicht das
Abrufen von Projektdetails bei einem Doppelklick und die Aktualisierung des ausgewählten Projekts.

Klassen:
--------
- UserEventHandlers: Verarbeitet Benutzerinteraktionen im Projekt-Treeview.

Funktionen innerhalb der Klasse:
--------------------------------
- __init__(self, project_frame, selected_frame): Initialisiert die Klasse mit Referenzen auf Frames.
- on_project_double_click(self, event): Verarbeitet Doppelklicks auf Projekte und aktualisiert den SelectedFrame.
- get_selected_project(self): Gibt die Projektdetails des ausgewählten Treeview-Elements zurück.

Verwendung:
-----------
    from feature_user_event_handlers import UserEventHandlers

    handler = UserEventHandlers(project_frame, selected_frame)
    project_frame.project_treeview.bind("<Double-1>", handler.on_project_double_click)
"""

class UserEventHandlers:
    """
    Eine Klasse für Ereignis-Handler im Benutzerinterface.

    Diese Klasse verarbeitet Doppelklick-Ereignisse auf Projekte im Treeview und aktualisiert
    den ausgewählten Projektbereich (SelectedFrame).
    """
    def __init__(self, project_frame, selected_frame):
        """
        Initialisiert die Klasse mit Referenzen auf die Frames.

        Args:
            project_frame: Der Frame, der die Projektliste enthält.
            selected_frame: Der Frame, der Details zum ausgewählten Projekt anzeigt.
        """
        self.project_frame = project_frame
        self.selected_frame = selected_frame

    def on_project_double_click(self, event):
        """
        Verarbeitet Doppelklicks auf ein Projekt in der Projektliste.

        - Ruft die Projektdetails des ausgewählten Projekts ab.
        - Aktualisiert den SelectedFrame mit den abgerufenen Projektdetails.

        Args:
            event: Das Doppelklick-Ereignis, ausgelöst durch den Benutzer.
        """
        project_number, project_name, description = self.get_selected_project()
        if project_number:
            # Aktualisiere den SelectedFrame
            self.selected_frame.update_project_details(
                selected_id=project_number,
                selected_name=project_name,
                description=description
            )
            self.selected_frame.master.selected_project_number = project_number
        else:
            print("Kein Projekt ausgewählt.")

    def get_selected_project(self):
        """
        Gibt die Details des ausgewählten Projekts im Treeview zurück.

        Returns:
            tuple: Ein Tupel bestehend aus Projektnummer, Projektname und Beschreibung.
                   Gibt (None, None, None) zurück, wenn kein Projekt ausgewählt ist.

        Fehlerbehandlung:
        ------------------
        - Gibt None-Werte zurück, falls kein Element im Treeview ausgewählt wurde.
        """
        try:
            selected_item = self.project_frame.project_treeview.selection()[0]
            project_values = self.project_frame.project_treeview.item(selected_item, 'values')
            print(f"Ausgewähltes Projekt: {project_values}")
            return project_values[0], project_values[1], project_values[2]
        except IndexError:
            return None, None, None
