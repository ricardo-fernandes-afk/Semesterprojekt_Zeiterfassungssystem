import customtkinter as ctk
from tkinter import messagebox
from db_connection import create_connection

def delete_user(user_id, refresh_callback):
    if not user_id:
        messagebox.showerror("Warnung", "Bitte wählen sie einen User zum löschen aus.")
        return
    
    confirmation = messagebox.askyesno("Bestätigung", "Sind Sie sicher, dass Sie diesen Benutzer löschen möchten?")
    if confirmation:
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
                connection.commit()
                messagebox.showinfo("Erfolg", "Benutzer erfolgreich gelöscht.")
                refresh_callback()
            except Exception as e:
                messagebox.showerror("Fehler", str(e))
            finally:
                cursor.close()
                connection.close()