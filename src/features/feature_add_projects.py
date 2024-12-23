import customtkinter as ctk
from tkinter import messagebox
from gui.gui_appearance_color import appearance_color, get_default_styles
from db.db_connection import create_connection

def add_project(admin_window, refresh_callback):
    colors = appearance_color()
    styles = get_default_styles()
    
    # Neues Fenster für die Projekterstellung
    project_window = ctk.CTkToplevel(admin_window)
    project_window.title("Neues Projekt erstellen")
    project_window.geometry("400x400")
    project_window.configure(fg_color=colors["background"])
    
    # Eingabefelder für den Projektnamen und die Beschreibung
    project_number_label = ctk.CTkLabel(project_window, text="Projektnummer", **styles["text"])
    project_number_label.pack(pady=10)
    project_number_entry = ctk.CTkEntry(project_window, **styles["entry"])
    project_number_entry.pack(pady=10)
    
    project_name_label = ctk.CTkLabel(project_window, text="Projektnamen", **styles["text"])
    project_name_label.pack(pady=10)
    project_name_entry = ctk.CTkEntry(project_window, **styles["entry"])
    project_name_entry.pack(pady=10)
    
    description_label = ctk.CTkLabel(project_window, text="Beschreibung", **styles["text"])
    description_label.pack(pady=10)
    description_entry = ctk.CTkEntry(project_window, **styles["entry"])
    description_entry.pack(pady=10)
    
    # Funktion, um das Projekt in die Datenbank einzufügen
    def save_project():
        project_name = project_name_entry.get()
        description = description_entry.get()
        project_number = project_number_entry.get()
        
        if project_number and project_name:
            connection = create_connection()
            if connection:
                cursor = connection.cursor()
                try:
                    cursor.execute("INSERT INTO projects (project_number, project_name, description) VALUES (%s, %s, %s)", (project_number, project_name, description))
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
    save_button = ctk.CTkButton(
        project_window,
        text="Speichern",
        command=save_project,
        **styles["button"],
        )
    save_button.pack(pady=20)
                    