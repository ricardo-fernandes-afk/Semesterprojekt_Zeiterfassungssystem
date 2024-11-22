import customtkinter as ctk
from db.db_connection import create_connection
from tkinter import messagebox
from features.feature_load_users import load_users

class UserToProjectFrame(ctk.CTkFrame):
    def __init__(self, master, selected_id):
        super().__init__(master, corner_radius=10)
        self.selected_id = selected_id

        # Label für User-Zuweisung
        label = ctk.CTkLabel(self, text="Benutzer zu Projekt zuweisen", font=("", 16, "bold"))
        label.pack(pady=10, padx=10, anchor="n")
        
        # User-Auswahl Dropdown
        self.user_dropdown = ctk.CTkComboBox(self)
        self.user_dropdown.pack(pady=10, fill="x", padx=10)
        
        # Zuweisen-Button
        assign_button = ctk.CTkButton(self, text="Benutzer zuweisen", command=self.assign_user_to_project)
        assign_button.pack(pady=10, anchor="s")

        self.load_users()

    def load_users(self):
        # Verwende die ausgelagerte Funktion `load_users`
        users = load_users()
        user_list = [f"{user[0]} - {user[1]}" for user in users]
        self.user_dropdown.configure(values=user_list)
    
    def assign_user_to_project(self):
        # Weisen Sie den ausgewählten Benutzer dem aktuell ausgewählten Projekt zu
        user_selection = self.user_dropdown.get()
        project_number = self.selected_id()

        if not user_selection:
            messagebox.showerror("Fehler", "Bitte wählen Sie einen Benutzer aus")
            return

        if not project_number:
            messagebox.showerror("Fehler", "Kein Projekt ausgewählt")
            return
        
        user_id = int(user_selection.split(" - ")[0])
        
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute(
                    "INSERT INTO user_projects (user_id, project_number) VALUES (%s, %s)",
                    (user_id, project_number)
                )
                connection.commit()
                messagebox.showinfo("Erfolg", "Benutzer erfolgreich zugewiesen")
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler bei der Zuweisung des Benutzers: {e}")
            finally:
                cursor.close()
                connection.close()
