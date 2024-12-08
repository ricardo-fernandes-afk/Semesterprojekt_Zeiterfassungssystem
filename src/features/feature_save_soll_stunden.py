from db.db_connection import create_connection
from tkinter import messagebox

def save_soll_stunden(self):
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