import customtkinter as ctk
from tkinter import messagebox
from db_connection import create_connection

# Hauptfenster für das Login
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.geometry("400x300")
root.title("Login mit CustomTkinter")

def open_user_interface(username):
    # Fenster für den Benutzer (User)
    user_window = ctk.CTkToplevel()
    user_window.title("User Interface")
    user_window.geometry("400x300")
    
    welcome_text = f"Willkommen, {username}!"
    ctk.CTkLabel(user_window, text = welcome_text).pack(pady=20)
    # Weitere Funktionen wie das Eintragen von Stunden können hier hinzugefügt werden
    
    user_window.mainloop()  # Startet den Loop für das neue Fenster
    
def open_admin_interface(username):
    # Fenster für den Admin
    admin_window = ctk.CTkToplevel()
    admin_window.title("Admin Interface")
    admin_window.geometry("400x300")
    
    welcome_text = f"Willkommen, Admin {username}!"
    ctk.CTkLabel(admin_window, text = welcome_text).pack(pady=20)
    # Weitere Funktionen wie das Hinzufügen von Projekten oder Benutzern können hier hinzugefügt werden
    
    admin_window.mainloop()  # Startet den Loop für das neue Fenster
    
def login():
    username = username_entry.get()
    password = password_entry.get()
    
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT role FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        if user:
            role = user[0]
            messagebox.showinfo("Erfolg", f"Login erfolgreich als {role}")
            
            root.destroy()
            
            if role == "user":
                open_user_interface(username)
            elif role == "admin":
                open_admin_interface(username)
            else:
                messagebox.showerror("Fehler", "Unbekannte Benutzerrolle")
        else:
            messagebox.showerror("Fehler", "Falscher Benutzername oder Passwort")
        
        cursor.close()
        connection.close()
        
# Benutzeroberfläche erstellen
frame = ctk.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label = ctk.CTkLabel(master=frame, text="Login", font=("Arial", 24))
label.pack(pady=12, padx=10)

username_entry = ctk.CTkEntry(master=frame, placeholder_text="Benutzername")
username_entry.pack(pady=12, padx=10)

password_entry = ctk.CTkEntry(master=frame, placeholder_text="Passwort", show="*")
password_entry.pack(pady=12, padx=10)

login_button = ctk.CTkButton(master=frame, text="Login", command=login)
login_button.pack(pady=12, padx=10)

root.mainloop()