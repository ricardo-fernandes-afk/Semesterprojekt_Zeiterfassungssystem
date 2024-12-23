import customtkinter as ctk
from tkinter import ttk, messagebox
from db.db_connection import create_connection
from gui.gui_appearance_color import appearance_color, get_default_styles, apply_treeview_style

class UserProjectFrame(ctk.CTkFrame):
    def __init__(self, master, username):
        self.colors = appearance_color()
        self.styles = get_default_styles()
        apply_treeview_style(self.colors)
        
        super().__init__(master, corner_radius=10, fg_color=self.colors["background"])
        self.username = username

        # Label für Projekte
        project_label = ctk.CTkLabel(master=self, text="Meine Projekte", **self.styles["title"])
        project_label.pack(pady=10, anchor="n")

        # Projektliste
        columns = ("Projektnummer", "Projektname", "Beschreibung")
        self.project_treeview = ttk.Treeview(self, columns=columns, show="headings")
        
        
        for col in columns:
            self.project_treeview.heading(col, text=col)
            self.project_treeview.column(col, width=200, stretch=True)
        
        self.project_treeview.pack(fill="both", expand=True, padx=10, pady=10)

        # Projekte laden
        self.load_user_projects()

    def load_user_projects(self):
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                query = """
                SELECT p.project_number, p.project_name, p.description
                FROM projects p
                JOIN user_projects up ON p.project_number = up.project_number
                JOIN users u ON up.user_id = u.user_id
                WHERE u.username = %s
                """
                cursor.execute(query, (self.username,))
                projects = cursor.fetchall()
                for project in projects:
                    self.project_treeview.insert("", "end", values=project)
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim Laden der Projekte: {e}")
            finally:
                cursor.close()
                connection.close()
