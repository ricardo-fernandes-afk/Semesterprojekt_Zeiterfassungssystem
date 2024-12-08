import customtkinter as ctk
from tkinter import messagebox, ttk
from db.db_connection import create_connection
from features.feature_add_projects import add_project
from features.feature_delete_project import delete_project, get_selected_project_number
 
class ProjectFrame(ctk.CTkFrame):
     
    def __init__(self, master):
        super().__init__(master, corner_radius=10)
    
        # Label für Projekte
        project_label = ctk.CTkLabel(master=self, text="Projekte", font=("", 18, "bold"))
        project_label.pack(pady=10, anchor="n")
        
        # Liste der Projekte
        columns = ("Projektnummer", "Projektname", "Beschreibung")
        self.project_treeview = ttk.Treeview(master=self, columns=columns, show="headings")
        
        self.update_idletasks()
        frame_width = self.winfo_width()
        
        num_columns = len(columns)
        if frame_width > 0:
            column_width = frame_width // num_columns
        else:
            column_width = 100
        
        for col in columns:
            self.project_treeview.heading(col, text=col)
            self.project_treeview.column(col, minwidth=50, width=column_width, stretch=True)
        
        self.project_treeview.pack(fill="both", expand=True, padx=10, pady=10, anchor="n")

        # Button zum Hinzufügen von Projekten
        add_project_button = ctk.CTkButton(master=self, text="Projekt hinzufügen", command=self.open_add_project_window)
        add_project_button.pack(pady=10, anchor="s")
        
         # Button zum Löschen von Projekten
        delete_project_button = ctk.CTkButton(master=self, text="Projekt Löchen", command=self.open_delete_project_window, fg_color="red")
        delete_project_button.pack(pady=10, anchor="s")
        
        self.load_projects()
        
    def get_selected_project_number(self):
        try:
            selected_item = self.project_treeview.selection()[0]  # Die ID des ausgewählten Elements abrufen
            project_values = self.project_treeview.item(selected_item, 'values')  # Die Werte des ausgewählten Projekts abrufen
            if len(project_values) >= 2:
                return project_values[0], project_values[1]  # `project_number` und `project_name` zurückgeben
            return None, None
        except IndexError:
            return None, None  # Keine Auswahl
        
    def load_projects(self):
        for item in self.project_treeview.get_children():
            self.project_treeview.delete(item)
            
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("SELECT project_number, project_name, description FROM projects")
                projects = cursor.fetchall()
                for project in projects:
                    self.project_treeview.insert("", "end", values=(project[0], project[1], project[2]))
                    
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim Laden der Projekte {e}")
                
            finally:
                cursor.close()
                connection.close()
                
    def open_add_project_window(self):
        add_project(self.master, self.load_projects)
        
    def open_delete_project_window(self):
        project_number = get_selected_project_number(self.project_treeview)
        if project_number is None:
            messagebox.showerror("Fehler", "Bitte wählen Sie ein Projekt aus")
            return
        
        confirmation = messagebox.askyesno("Bestätigung", "Sind Sie sicher, dass Sie dieses Projekt löschen möchten?")
        if confirmation:
            delete_project(project_number, self.load_projects)