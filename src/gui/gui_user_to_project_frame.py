import customtkinter as ctk
from db.db_connection import create_connection
from tkinter import messagebox, ttk
from features.feature_load_users import load_users
from features.feature_load_project_users import load_project_users

class UserToProjectFrame(ctk.CTkFrame):
    def __init__(self, master, project_number):
        super().__init__(master, corner_radius=10)
        self.project_number = project_number
        self.available_users = []
        self.project_users = []
        self.create_widgets()
        self.load_users()
        self.load_project_users()

    def create_widgets(self):
        # Label für User-Zuweisung
        self.label = ctk.CTkLabel(self, text="Benutzer zu Projekt zuweisen", font=("", 16, "bold"))
        self.label.grid(row=0, pady=10, padx=10, sticky="nsew")
        
        # User-Auswahl Dropdown
        self.user_dropdown = ctk.CTkComboBox(self)
        self.user_dropdown.grid(row=1, padx=10, sticky="nsew")
        
        # Zuweisen-Button
        self.assign_button = ctk.CTkButton(self, text="Benutzer zuweisen", command=self.assign_user_to_project)
        self.assign_button.grid(row=2, pady=5, sticky="nsew")
        
        # Label für vorhandene Benutzer
        self.project_users_label = ctk.CTkLabel(self, text="Benutzer im Projekt", font=("", 14))
        self.project_users_label.grid(row=3, padx=10, sticky="nsew")
        
        # Treeview für die Liste der Benutzer im Projekt
        self.users_treeview = ttk.Treeview(self, columns=("user_id", "username"), show="headings", height=8)
        self.users_treeview.heading("user_id", text="Benutzer-ID")
        self.users_treeview.heading("username", text="Benutzername")
        self.users_treeview.grid(row=4, pady=5, padx=10, sticky="nsew")
        
        # Löschen-Button
        self.delete_button = ctk.CTkButton(self, text="Benutzer entfernen", fg_color="red", command=self.delete_user_from_project)
        self.delete_button.grid(row=5, pady=(0,10), padx=10, sticky="nsew")

    def load_users(self):
        # Verwende die ausgelagerte Funktion `load_users`
        users = load_users()
        self.available_users = [f"{user[0]} - {user[1]}" for user in users]
        self.user_dropdown.configure(values=self.available_users)
        
    def load_project_users(self):
        # Benutzer, die bereits dem Projekt zugeordnet sind, aus der Datenbank laden
        users = load_project_users(self.project_number)
        self.project_users = users
        self.update_users_treeview()
    
    def update_users_treeview(self):
        # Die Liste der Benutzer im Projekt aktualisieren
        for item in self.users_treeview.get_children():
            self.users_treeview.delete(item)
        for user in self.project_users:
            self.users_treeview.insert("", "end", values=(user[0], user[1]))        
    
    def assign_user_to_project(self):
        # Weisen Sie den ausgewählten Benutzer dem aktuell ausgewählten Projekt zu
        user_selection = self.user_dropdown.get()
        if not user_selection:
            messagebox.showerror("Fehler", "Bitte wählen Sie einen Benutzer aus")
            return
        
        user_id = int(user_selection.split(" - ")[0])
        
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute(
                    "INSERT INTO user_projects (user_id, project_number) VALUES (%s, %s)",
                    (user_id, self.project_number)
                )
                connection.commit()
                messagebox.showinfo("Erfolg", "Benutzer erfolgreich zugewiesen")
                self.load_project_users()  # Aktualisiere die Liste der Projekt-Benutzer
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler bei der Zuweisung des Benutzers: {e}")
            finally:
                cursor.close()
                connection.close()
    
    def delete_user_from_project(self):
        # Benutzer aus Projekt entfernen
        selected_item = self.users_treeview.selection()
        if not selected_item:
            messagebox.showerror("Fehler", "Bitte wählen Sie einen Benutzer aus der Liste aus")
            return

        user_id = self.users_treeview.item(selected_item, "values")[0]
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute(
                    "DELETE FROM user_projects WHERE user_id = %s AND project_number = %s",
                    (user_id, self.project_number)
                )
                connection.commit()
                messagebox.showinfo("Erfolg", "Benutzer erfolgreich entfernt")
                self.load_project_users()  # Aktualisiere die Liste der Projekt-Benutzer
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim Entfernen des Benutzers: {e}")
            finally:
                cursor.close()
                connection.close()
