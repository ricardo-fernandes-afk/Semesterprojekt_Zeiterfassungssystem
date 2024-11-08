import customtkinter as ctk
from tkinter import messagebox, ttk
from db_connection import create_connection
from feature_add_projects import add_project
 
class ProjectFrame(ctk.CTkFrame):
     
    def __init__(self, master):
        super().__init__(master, corner_radius=10)
        self.grid(row=1, column=0, rowspan=4, padx=10, pady=10, sticky="nsw")
    
        # Label für Projekte
        project_label = ctk.CTkLabel(master=self, text="Projekte", font=("", 18))
        project_label.pack(pady=10)
        
        # Liste der Projekte
        columns = ("ID", "Projektname", "Beschreibung")
        self.project_treeview = ttk.Treeview(master=self, columns=columns, show="headings")
        
        for col in columns:
            self.project_treeview.heading(col, text=col)
            self.project_treeview.column(col, anchor="w")
        
        self.project_treeview.pack(padx=10, fill="both", expand=True)
        
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
        
        self.load_projects()
        
        # Button zum Hinzufügen von Projekten
        add_project_button = ctk.CTkButton(master=self, text="Projekt hinzufügen", command=self.open_add_project_window)
        add_project_button.pack(pady=10)
        
    def load_projects(self):
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("SELECT project_id, project_name, description FROM projects")
                projects = cursor.fetchall()
                for project in projects:
                    self.project_treeview.insert("", "end", values=(project[0], project[1], project[2]))
                    
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim Laden der Projekte {e}")
                
            finally:
                connection.close()
        
    def open_add_project_window(self):
        add_project(self.master)