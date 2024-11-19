import customtkinter as ctk
from tkinter import ttk
from tkinter import messagebox
from db.db_connection import create_connection

def get_selected_user_id(treeview):
    selected_item = treeview.selection()    # Liefert die ID des ausgewählten Treeview-Eintrags
    if not selected_item:
        return None
    
    # Hole die Daten des ausgewählten Eintrags
    user_data = treeview.item(selected_item)
    user_values = user_data.get("values")
    
    # Sicherstellen, dass wir tatsächlich Werte erhalten und die Benutzer-ID korrekt extrahieren
    if user_values and len(user_values) > 0:
        return user_values[0]
    return None      

def delete_user(user_id, refresh_callback):
    connection = create_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
                connection.commit()
                messagebox.showinfo("Erfolg", "Benutzer erfolgreich gelöscht.")
                refresh_callback()
        except Exception as e:
            messagebox.showerror("Fehler", str(e))
        finally:
            connection.close()