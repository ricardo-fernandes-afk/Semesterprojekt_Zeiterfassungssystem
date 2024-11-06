import customtkinter as ctk

def open_user_interface(username):
    # Fenster für den Benutzer (User)
    user_window = ctk.CTkToplevel()
    user_window.title("User Interface")
    user_window.geometry("400x300")
    
    welcome_text = f"Willkommen, {username}!"
    ctk.CTkLabel(user_window, text = welcome_text).pack(pady=20)
    # Weitere Funktionen wie das Eintragen von Stunden können hier hinzugefügt werden
    
    user_window.mainloop()  # Startet den Loop für das neue Fenster
    