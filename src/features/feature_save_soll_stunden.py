from db.db_connection import create_connection
from tkinter import messagebox

def save_soll_stunden(self):
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            for phase in self.phase_labels:
                soll_stunden = self.soll_stunden_entries[phase].get()
                try:
                    cursor.execute('''INSERT INTO project_sia_phases (project_number, phase_name, soll_stunden)
                                      VALUES (%s, %s, %s)
                                      ON CONFLICT (project_number, phase_name) DO UPDATE SET soll_stunden = EXCLUDED.soll_stunden;''', 
                                   (self.project_number, phase, soll_stunden))
                except Exception as e:
                    messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten: {e}")
            connection.commit()
            messagebox.showinfo("Erfolg", "Soll-Stunden erfolgreich gespeichert.")
            cursor.close()
            connection.close()