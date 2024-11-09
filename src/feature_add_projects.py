import customtkinter as ctk
from tkinter import messagebox
from gui_appearance_color import appearance_color
from db_connection import create_connection

def add_project(admin_window, refresh_callback):
    appearance_color()
    
    # Neues Fenster für die Projekterstellung
    project_window = ctk.CTkToplevel(admin_window)
    project_window.title("Neues Projekt erstellen")
    project_window.geometry("400x400")
    
    # Eingabefelder für den Projektnamen und die Beschreibung
    project_id_label = ctk.CTkLabel(project_window, text="Projektnummer:")
    project_id_label.pack(pady=10)
    project_id_entry = ctk.CTkEntry(project_window)
    project_id_entry.pack(pady=10)
    
    project_name_label = ctk.CTkLabel(project_window, text="Projektnamen:")
    project_name_label.pack(pady=10)
    project_name_entry = ctk.CTkEntry(project_window)
    project_name_entry.pack(pady=10)
    
    description_label = ctk.CTkLabel(project_window, text="Beschreibung:")
    description_label.pack(pady=10)
    description_entry = ctk.CTkEntry(project_window)
    description_entry.pack(pady=10)
    
    # Funktion, um das Projekt in die Datenbank einzufügen
    def save_project():
        project_name = project_name_entry.get()
        description = description_entry.get()
        project_id = project_id_entry.get()
        
        if project_id and project_name:
            connection = create_connection()
            if connection:
                cursor = connection.cursor()
                try:
                    cursor.execute("INSERT INTO projects (project_id, project_name, description) VALUES (%s, %s, %s)", (project_id, project_name, description))
                    connection.commit()
                    messagebox.showinfo("Projekt erstellt", "Das Projekt wurde erfolgreich erstellt.")
                    refresh_callback()
                    project_window.destroy() # Fenster schließen, wenn das Projekt erfolgreich hinzugefügt wurde
                except:
                    messagebox.showerror("Fehler", "Ein Fehler ist aufgetreten. Bitte überprüfen!")
                finally:
                    cursor.close()
                    connection.close()
        else:
            messagebox.showerror("Fehler", "Bitte geben Sie einen Projektnamen ein.")

    # Button zum speichern des Projekts
    save_button = ctk.CTkButton(project_window, text="Speichern", command=save_project)
    save_button.pack(pady=20)
                    