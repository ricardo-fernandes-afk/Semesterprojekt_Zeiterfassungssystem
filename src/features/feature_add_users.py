import customtkinter as ctk
from tkinter import messagebox
from db.db_connection import create_connection
from gui.gui_appearance_color import appearance_color, get_default_styles

def add_user(admin_window, refresh_callback):
    colors = appearance_color()
    styles = get_default_styles()
    
    # Neues Fenster für die Benutzererstellung
    user_window = ctk.CTkToplevel(admin_window)
    user_window.title("Neuen Benutzer erstellen")
    user_window.geometry("400x400")
    user_window.configure(fg_color=colors["background"])
    
    # Eingabefelder für den Benutzernamen
    username_label = ctk.CTkLabel(user_window, text="Benutzername", **styles["text"])
    username_label.pack(pady=10)
    username_entry = ctk.CTkEntry(user_window, **styles["entry"])
    username_entry.pack(pady=10)
    
    # Eingabefelder für das Password des Users
    password_label = ctk.CTkLabel(user_window, text="Password", **styles["text"])
    password_label.pack(pady=10)
    password_entry = ctk.CTkEntry(user_window, **styles["entry"])
    password_entry.pack(pady=10)
    
    # Auswahl der Rolle des Users
    role_label = ctk.CTkLabel(user_window, text="Rolle", **styles["text"])
    role_label.pack(pady=10)
    
    role_var = ctk.StringVar(value="user", **styles["text"])     # Standardwert auf "User " setzen
    role_option = ctk.CTkOptionMenu(user_window, values=["user", "admin"], variable=role_var)
    role_option.pack(pady=10)
    
    def save_user():
        user_name = username_entry.get()
        user_password = password_entry.get()
        user_role = role_var.get()
        
        if user_name:
            connection = create_connection()
            if connection:
                cursor = connection.cursor()
                try:
                    cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",(user_name, user_password, user_role))
                    connection.commit()
                    messagebox.showinfo("User erstellt", "User wurde erfolgreich erstellt.")
                    refresh_callback()
                    user_window.destroy()   # Fenster schließen, wenn der User erfolgreich hinzugefügt wurde
                except:
                    messagebox.showerror("Fehler", "Fehler bei der Erstellung des Users.")
                finally:
                    cursor.close()
                    connection.close()
        else:
            messagebox.showerror("Fehler", "Bitte geben Sie einen Benutzernamen ein.")
            
    # Button zum Speichern des neuen Benutzers
    save_button = ctk.CTkButton(
        user_window,
        text="Speichern",
        command=save_user,
        **styles["button"],
        )
    save_button.pack(pady=20)