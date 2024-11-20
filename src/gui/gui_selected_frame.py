import customtkinter as ctk 
from tkinter import messagebox, ttk
from db.db_connection import create_connection

class SelectedFrame(ctk.CTkFrame):
    def __init__(self, master, selected_id=None, selected_name=None):
        super().__init__(master, corner_radius=10)
        self.selected_id = selected_id
        self.selected_name = selected_name
        self.description = None
        self.create_widgets()
    
    def create_widgets(self):
        # Platzhalter für Projektdetails
        self.title_label = ctk.CTkLabel(self, text=f"{self.selected_id} {self.selected_name}" if self.selected_name else "Wählen Sie ein Projekt oder einen Benutzer", font=("", 20))
        self.title_label.pack(pady=20)
        
    def update_project_details(self, selected_id, selected_name, description=None):
        # Widgets entfernen, um Platz für neue Details zu schaffen
        for widget in self.winfo_children():
            widget.destroy()

        # Neue Projektdetails anzeigen
        self.selected_id = selected_id
        self.selected_name = selected_name
        self.description = description

        self.title_label = ctk.CTkLabel(self, text=f"{self.selected_id} - {self.selected_name}", font=("", 24))        
        self.title_label.pack(pady=(5,5))

        if self.description:
            ctk.CTkLabel(self, text=self.description, font=("", 16), wraplength=300).pack(pady=(5, 5))
        
