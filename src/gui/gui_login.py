"""
Modul: Login-GUI für TimeArch.

Dieses Modul stellt eine grafische Benutzeroberfläche für den Login bereit. Es validiert die Benutzereingaben und authentifiziert den Benutzer anhand der Datenbank. Je nach Benutzerrolle wird die entsprechende GUI gestartet (Admin oder Benutzer).

Klassen:
--------
- LoginGUI: Hauptklasse zur Verwaltung des Login-Interfaces.

Methoden:
---------
- __init__(self, master): Initialisiert die Login-GUI mit Benutzereingabe- und Steuerungsfeldern.
- login(self): Authentifiziert den Benutzer anhand von Benutzername und Passwort.
- on_closing(self): Schließt die Anwendung.

Verwendung:
-----------
    from gui_login import LoginGUI

    root = ctk.CTk()
    app = LoginGUI(master=root)
    root.mainloop()
"""

import customtkinter as ctk
from tkinter import messagebox, PhotoImage
from PIL import Image, ImageTk
from db.db_connection import create_connection
from gui.gui_appearance_color import appearance_color, get_default_styles

class LoginGUI:
    """
    Eine Klasse zur Verwaltung des Login-Interfaces.

    Funktionen:
    - Validierung von Benutzereingaben
    - Authentifizierung über die Datenbank
    - Start der entsprechenden GUI basierend auf der Benutzerrolle
    """
    def __init__(self, master):
        """
        Initialisiert die Login-GUI mit Eingabe- und Steuerungsfeldern.

        Args:
            master (ctk.CTk): Das übergeordnete Fenster.
        """
        self.master = master
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
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
        """
        Authentifiziert den Benutzer anhand von Benutzername und Passwort.

        - Überprüft, ob alle Felder ausgefüllt sind.
        - Führt eine Datenbankabfrage durch, um die Benutzerrolle und ID zu ermitteln.
        - Startet die entsprechende GUI basierend auf der Benutzerrolle.

        Fehlerbehandlung:
        ------------------
        - Zeigt Warnungen oder Fehlermeldungen bei unvollständigen Eingaben oder ungültigen Anmeldedaten an.
        """
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
    
    def on_closing(self):
        """
        Schließt die Anwendung.

        - Zerstört das Hauptfenster.
        """
        self.master.destroy()