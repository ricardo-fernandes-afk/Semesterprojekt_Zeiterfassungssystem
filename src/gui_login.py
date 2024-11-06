import customtkinter as ctk
from tkinter import messagebox
from db_connection import create_connection
from gui_admin import create_admin_layout
from gui_users import create_users_layout

# Hauptfenster für das Login
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.geometry("600x400")
root.title("Login mit CustomTkinter")



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
                create_users_layout(username)
            elif role == "admin":
                create_admin_layout(username)
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