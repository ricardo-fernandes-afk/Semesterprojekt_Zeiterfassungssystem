import customtkinter as ctk

def open_admin_interface(username):
    # Fenster für den Admin
    admin_window = ctk.CTkToplevel()
    admin_window.title("Admin Interface")
    admin_window.geometry("400x300")
    
    welcome_text = f"Willkommen, Admin {username}!"
    ctk.CTkLabel(admin_window, text = welcome_text).pack(pady=20)
    # Weitere Funktionen wie das Hinzufügen von Projekten oder Benutzern können hier hinzugefügt werden
    
    admin_window.mainloop()  # Startet den Loop für das neue Fenster
    
    
    