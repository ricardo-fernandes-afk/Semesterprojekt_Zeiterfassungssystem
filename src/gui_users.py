import customtkinter as ctk
from tkinter import messagebox
from db_connection import create_connection

def create_users_layout(username):
    # Fenster für den Benutzer (User)
    user_window = ctk.CTk()
    user_window.title("User Interface")
    user_window.geometry("600x400")
    
    welcome_text = f"Willkommen, {username}!"
    ctk.CTkLabel(user_window, text = welcome_text, font=("Century Gothic", 20)).grid(row=0, column=0, columnspan=2, pady=10)
    # Weitere Funktionen wie das Eintragen von Stunden können hier hinzugefügt werden
    
    user_window.mainloop()  # Startet den Loop für das neue Fenster
    