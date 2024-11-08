import customtkinter as ctk
from tkinter import messagebox
from db_connection import create_connection
from gui_appearance_color import appearance_color

class LoginGUI:
    def __init__(self, master):
        self.master = master
        appearance_color()
        
        self.master.geometry("600x400")
        self.master.title("Login mit CustomTkinter")
        
        self.label = ctk.CTkLabel(self.master, text="Login", font=("", 24))
        self.label.pack(pady=12)
        
        self.username_entry = ctk.CTkEntry(self.master, placeholder_text="Benutzername")
        self.username_entry.pack(pady=20)
        
        self.password_entry = ctk.CTkEntry(self.master, placeholder_text="Passwort", show="*")
        self.password_entry.pack(pady=10)
        
        self.login_button = ctk.CTkButton(self.master, text="Login", command=self.login)
        self.login_button.pack(pady=10)
        
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showwarning("Warnung", "Bitte Benutzername und Passwort eingeben.")
            return
        try:
            connection = create_connection()
            if connection:
                cursor = connection.cursor()
                cursor.execute("SELECT role FROM users WHERE username = %s AND password = %s", (username, password))
                user = cursor.fetchone()
                if user:
                    role = user[0]
                    messagebox.showinfo("Erfolg", f"Login erfolgreich als {role}")
                    
                    self.master.destroy()
                    
                    if role == "user":
                        from gui_users import start_user_gui
                        start_user_gui(username)
                    elif role == "admin":
                        from gui_admin import start_admin_gui
                        start_admin_gui(username)
                    else:
                        messagebox.showerror("Fehler", f"Unbekannte Benutzerrolle: Die Rolle '{role}' ist nicht definiert.")
                else:
                    messagebox.showerror("Fehler", "Falscher Benutzername oder Passwort")
                    
        except Exception as e:
            messagebox.showerror("Fehler", str(e))
        
        finally:
            if connection:   
                cursor.close()
                connection.close()