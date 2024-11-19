import customtkinter as ctk 
from tkinter import messagebox, ttk
from db.db_connection import create_connection

class SelectedProject(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=10)