import customtkinter as ctk
from tkinter import messagebox
from db_connection import create_connection

def create_admin_layout(username):
    # Fenster für den Admin
    admin_window = ctk.CTk()
    admin_window.title("Admin Interface")
    admin_window.geometry("600x400")
    
    welcome_text = f"Willkommen, Admin {username}!"
    ctk.CTkLabel(admin_window, text = welcome_text, font=("Century Gothic", 20)).grid(row=0, column=0, columnspan=2, pady=10)
    
    project_frame = ctk.CTkFrame(master=admin_window)
    project_frame.pack(pady=20, padx=20, fill="both", expand=True)
    
    project_label = ctk.CTkLabel(master=project_frame, text="Projekte", font=("Century Gothic", 16))
    project_label.pack(pady=10)
    
    add_project_button = ctk.CTkButton(master=project_frame, text="Projekt hinzufügen")
    add_project_button.pack(pady=10)
    
    admin_window.mainloop()  # Startet den Loop für das neue Fenster
    
    
if __name__ == "__main__":
    create_admin_layout()  