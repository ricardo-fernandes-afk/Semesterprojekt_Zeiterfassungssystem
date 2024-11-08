import customtkinter as ctk
from tkinter import messagebox, ttk
from db_connection import create_connection
from feature_add_projects import add_project

def create_admin_layout(username):
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")
    # Fenster für den Admin
    admin_window = ctk.CTk()
    admin_window.title("Admin Interface")
    admin_window.geometry("1200x800")
    
    welcome_text = f"Willkommen, Admin {username}!"
    ctk.CTkLabel(admin_window, text = welcome_text, font=("Arial", 20)).grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky="w")
    
    # Frame für Projekte
    admin_window.grid_columnconfigure(0, weight=1)
    admin_window.grid_columnconfigure(1, weight=4)
    admin_window.rowconfigure(1, weight=1)
    
    project_frame = ctk.CTkFrame(master=admin_window, corner_radius=10)
    project_frame.grid(row=1, column=0, rowspan=4, padx=10, pady=10, sticky="nsw")
    
    # Label für Projekte
    project_label = ctk.CTkLabel(master=project_frame, text="Projekte", font=("", 18))
    project_label.pack(pady=10)
    
    # Liste der Projekte
    columns = ("ID", "Projektname", "Beschreibung")
    project_treeview = ttk.Treeview(master=project_frame, columns=columns, show="headings")
    
    for col in columns:
        project_treeview.heading(col, text=col)
        project_treeview.column(col, anchor="w")
    
    project_treeview.pack(padx=10, fill="both", expand=True)
    
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
    
    def load_projects():
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("SELECT project_id, project_name, description FROM projects")
                projects = cursor.fetchall()
                for project in projects:
                    project_treeview.insert("", "end", values=(project[0], project[1], project[2]))
                    
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim Laden der Projekte {e}")
                
            finally:
                connection.close()
    
    load_projects()
    
    # Button zum Hinzufügen von Projekten
    add_project_button = ctk.CTkButton(master=project_frame, text="Projekt hinzufügen", command=lambda: add_project(admin_window))
    add_project_button.pack(pady=10)
    
    # Startet den Loop für das neue Fenster
    admin_window.mainloop()
    
if __name__ == "__main__":
    create_admin_layout()