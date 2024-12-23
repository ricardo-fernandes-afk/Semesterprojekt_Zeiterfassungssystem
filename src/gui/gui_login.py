import customtkinter as ctk
from tkinter import messagebox, PhotoImage
from PIL import Image, ImageTk
from db.db_connection import create_connection
from gui.gui_appearance_color import appearance_color, get_default_styles

class LoginGUI:
    def __init__(self, master):
        self.master = master
        colors = appearance_color()
        styles = get_default_styles()
        
        self.master.geometry("600x400")
        self.master.title("TimeArch - More Time for Visions")
        self.master.configure(bg=colors["background"])
        
        icon_path = "C:/Users/ricar/OneDrive/Dokumente/VS_Projects/Semesterprojekt_Zeiterfassungssystem/docs/Logo_TimeArch.ico"
        self.master.iconbitmap(icon_path)
        
        self.label = ctk.CTkLabel(self.master, text="Login", **styles["title"])
        self.label.pack(pady=12)
        
        self.username_entry = ctk.CTkEntry(self.master, placeholder_text="Benutzername", **styles["entry"])
        self.username_entry.pack(pady=20)
        
        self.password_entry = ctk.CTkEntry(self.master, placeholder_text="Passwort", show="*", **styles["entry"])
        self.password_entry.pack(pady=10)
        
        self.login_button = ctk.CTkButton(self.master, text="Login", **styles["button"], command=self.login)
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
                cursor.execute("SELECT role, user_id FROM users WHERE username = %s AND password = %s", (username, password))
                user = cursor.fetchone()
                if user:
                    role, user_id = user
                    messagebox.showinfo("Erfolg", f"Login erfolgreich als {role}")
                    
                    self.master.destroy()
                    
                    if role == "user":
                        from gui.user.gui_users import start_user_gui
                        start_user_gui(username, user_id)
                    elif role == "admin":
                        from gui.admin.gui_admin import start_admin_gui
                        start_admin_gui(username, user_id)
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