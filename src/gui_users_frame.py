import customtkinter as ctk
from tkinter import messagebox, ttk
from db_connection import create_connection
from feature_add_users import add_user
from feature_delete_users import delete_user

class UserFrame(ctk.CTkFrame):
    
    def __init__(self, master):
        super().__init__(master, corner_radius=10)
        self.grid(row=1, column=1, padx=1, pady=10, sticky="nsw")
        
        # Label für Users
        user_label = ctk.CTkLabel(master=self, text="Users", font=("", 18))
        user_label.grid(row=0, column=0, pady=10)
        
        # Liste der Users
        columns = ("ID", "Username", "Password", "Role")
        self.user_treeview = ttk.Treeview(master=self, columns=columns, show="headings")
        
        for col in columns:
            self.user_treeview.heading(col, text=col)
            self.user_treeview.column(col, anchor="w")
            
        self.user_treeview.grid(row=1, column=0, padx=10, sticky="nsew")
        
        style = ttk.Style()
        style.theme_use('clam')
        
        bg_color = "#2e2e2e"  # Dark background color
        fg_color = "white"
        
        style.configure("Treeview",
                        background=bg_color,
                        foreground=fg_color,
                        rowheight=25,
                        fieldbackground=bg_color)
        style.map("Treeview",
                background=[("selected", "#0078d7")],
                foreground=[("selected", "white")])
        
        # Button zum Hinzufügen und Löschen von User
        add_button = ctk.CTkButton(self, text="Benutzer hinzufügen", command=self.open_add_user_window)
        add_button.grid(row=2, column=0, pady=10)
        
        delete_button = ctk.CTkButton(self, text="Benutzer löschen", command=self.open_delete_user_window, bg_color="red")
        delete_button.grid(row=3, column=0, pady=10)
        
        self.load_users()
        
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
        delete_user(self.master, self.load_users)