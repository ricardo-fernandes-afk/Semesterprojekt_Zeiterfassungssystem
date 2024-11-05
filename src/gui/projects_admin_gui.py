import customtkinter as ctk
from tkinter import messagebox
from src.db.db_connection import create_connection

def create_project_frame_admin(admin_window):
    
    # Frame für Projektliste
    project_frame = ctk.CTkFrame(admin_window, corner_radius=10, fg_color="#")
    project_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Label für die Projekte
    project_label = ctk.CTkLabel(project_frame, text="Projekte", font=("Century Gothic", 16))
    project_label.pack(pady=10)