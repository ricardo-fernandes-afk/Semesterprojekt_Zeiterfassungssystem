from db.db_connection import create_connection
from tkinter import messagebox

def load_soll_stunden(self):
        # Hier laden wir die Soll-Stunden aus der Datenbank
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