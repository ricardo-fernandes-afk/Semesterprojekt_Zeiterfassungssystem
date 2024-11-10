import customtkinter as ctk
from tkinter import messagebox, ttk
from db_connection import create_connection
from feature_add_users import add_user
from feature_delete_users import delete_user

class UserFrame(ctk.CTkFrame):
    
    def __init__(self, master):
        super().__init__(master, corner_radius=10)
        
        # Label für Users
        user_label = ctk.CTkLabel(master=self, text="Users", font=("", 18))
        user_label.pack(pady=10, anchor="n")
        
        # Liste der Users
        columns = ("ID", "Username", "Password", "Role")
        self.user_treeview = ttk.Treeview(master=self, columns=columns, show="headings")
        
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
        add_button.pack(pady=10, anchor="s")
        
        delete_button = ctk.CTkButton(self, text="Benutzer löschen", command=self.open_delete_user_window, fg_color="red")
        delete_button.pack(pady=10, anchor="s")
        
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