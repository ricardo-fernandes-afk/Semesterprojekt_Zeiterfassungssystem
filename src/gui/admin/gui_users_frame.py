import customtkinter as ctk
from tkinter import messagebox, ttk
from db.db_connection import create_connection
from features.feature_add_users import add_user
from features.feature_delete_users import delete_user, get_selected_user_id
from gui.gui_appearance_color import appearance_color, get_default_styles, apply_treeview_style

class UserFrame(ctk.CTkFrame):
    def __init__(self, master):
        self.colors = appearance_color()
        self.styles = get_default_styles()
        
        super().__init__(master, corner_radius=10, fg_color=self.colors["background"])
        
        # Label für Users
        user_label = ctk.CTkLabel(master=self, text="Benutzer", **self.styles["title"])
        user_label.pack(pady=10, anchor="n")
        
        # Liste der Users
        columns = ("ID", "Username", "Password", "Role")
        self.user_treeview = ttk.Treeview(master=self, columns=columns, show="headings")
        apply_treeview_style(self.colors)
        
        self.update_idletasks()
        frame_width = self.winfo_width()
        
        num_columns = len(columns)
        if frame_width > 0:
            column_width = frame_width // num_columns
        else:
            column_width = 100
        
        for col in columns:
            self.user_treeview.heading(col, text=col)
            self.user_treeview.column(col, minwidth=50, width=column_width, stretch=True)
            
        self.user_treeview.pack(fill="both", expand=True, padx=10, pady=10, anchor="n")
        
        # Button zum Hinzufügen und Löschen von User
        add_button = ctk.CTkButton(
            self,
            text="Benutzer hinzufügen",
            command=self.open_add_user_window,
            **self.styles["button"]
        )
        add_button.pack(pady=10, anchor="s")
        
        delete_button = ctk.CTkButton(
            self,
            text="Benutzer löschen",
            command=self.open_delete_user_window,
            fg_color=self.colors["error"],
            hover_color=self.colors["warning"],
        )
        delete_button.pack(pady=10, anchor="s")
        
        self.load_users()
        
    def get_selected_user(self):
        try:
            selected_item = self.user_treeview.selection()[0]  # Die ID des ausgewählten Elements abrufen
            user_values = self.user_treeview.item(selected_item, 'values')  # Die Werte des ausgewählten Benutzers abrufen
            if len(user_values) >= 1:
                return int(user_values[0]), user_values[1]  # `user_id` und `username` zurückgeben
            return None, None
        except IndexError:
            return None, None  # Keine Auswahl
        
    def load_users(self):
        for item in self.user_treeview.get_children():
            self.user_treeview.delete(item)
            
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("SELECT user_id, username, password, role FROM users")
                users = cursor.fetchall()
                for user in users:
                    self.user_treeview.insert("", "end", values=(user[0], user[1], user[2], user[3]))
                    
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim Laden der Projekte {e}")
                
            finally:
                cursor.close()
                connection.close()
    
    def open_add_user_window(self):
        add_user(self.master, self.load_users)
        
    def open_delete_user_window(self):
        user_id = get_selected_user_id(self.user_treeview)
        if user_id is None:
            messagebox.showerror("Fehler", "Bitte wählen Sie einen Benutzer aus")
            return
        
        confirmation = messagebox.askyesno("Bestätigung", "Sind Sie sicher, dass Sie diesen Benutzer löschen möchten?")
        if confirmation:
            delete_user(user_id, self.load_users)