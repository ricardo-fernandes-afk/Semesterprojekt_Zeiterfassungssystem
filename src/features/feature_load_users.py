from db.db_connection import create_connection
from tkinter import messagebox

def load_users():
    users = []
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT user_id, username FROM users")
            users = cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Laden der Benutzer: {e}")
        finally:
            cursor.close()
            connection.close()
    
    return users
