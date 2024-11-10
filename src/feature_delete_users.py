import customtkinter as ctk
from tkinter import ttk
from tkinter import messagebox
from db_connection import create_connection

def get_selected_user_id(treeview):
    selected_item = treeview.selection()    # Liefert die ID des ausgewählten Treeview-Eintrags
    if not selected_item:
        return None
    
    # Hole die Daten des ausgewählten Eintrags
    user_data = treeview.item(selected_item)
    user_values = user_data.get("values")
    
    # Sicherstellen, dass wir tatsächlich Werte erhalten und die Benutzer-ID korrekt extrahieren
    if user_values and len(user_values) > 0:
        user_id = user_values[0]
        
        print(f"Vor Konvertierung - Benutzer ID {user_id}, Typ: {type(user_id)}")
        try:
            user_id = int(user_values[0])
            print(f"Nach Konvertierung - Benutzer-ID: {user_id}, Typ: {type(user_id)}")
            return user_id
        except ValueError:
            messagebox.showerror("Fehler", "Benutzer-ID ist kein gültiger Integer")
            return None
    return None
        

def delete_user(user_id, refresh_callback):
    if not isinstance (user_id, int):
        messagebox.showerror("Warnung", "Benutzer-ID ist kein gültiger Typ.")
        return
    
    confirmation = messagebox.askyesno("Bestätigung", "Sind Sie sicher, dass Sie diesen Benutzer löschen möchten?")
    if confirmation:
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