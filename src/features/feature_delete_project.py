import customtkinter as ctk
from tkinter import ttk
from tkinter import messagebox
from db.db_connection import create_connection

def get_selected_project_number(treeview):
    selected_item = treeview.selection()    # Liefert die ID des ausgewählten Treeview-Eintrags
    if not selected_item:
        return None
    
    # Hole die Daten des ausgewählten Eintrags
    project_data = treeview.item(selected_item)
    project_values = project_data.get("values")
    
    # Sicherstellen, dass wir tatsächlich Werte erhalten und die Benutzer-ID korrekt extrahieren
    if project_values and len(project_values) > 0:
        return project_values[0]
    return None      

def delete_project(project_number, refresh_callback):
    connection = create_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM projects WHERE project_number = %s", (project_number,))
                connection.commit()
                messagebox.showinfo("Erfolg", "Projekt erfolgreich gelöscht.")
                refresh_callback()
        except Exception as e:
            messagebox.showerror("Fehler", str(e))
        finally:
            connection.close()