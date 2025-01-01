import customtkinter as ctk
from datetime import date
from tkinter import messagebox
from db.db_connection import create_connection
from gui.gui_appearance_color import appearance_color, get_default_styles

class InternInfosFrame(ctk.CTkFrame):
    def __init__(self, master, user_id=None, username=None):
        self.colors = appearance_color()
        self.styles = get_default_styles()
        super().__init__(master, corner_radius=10, fg_color=self.colors["alt_background"])
        
        self.user_id = user_id
        self.username = username
        self.start_date = None
        self.default_hours_per_day = None
        self.employment_percentage = None
        self.vacation_days = None
        self.create_widgets()
        if self.user_id:
            self.load_user_settings()
        
    def create_widgets(self):
        for col in range(4):
            self.grid_columnconfigure(col, weight=1)
        for row in range(2):
            self.grid_rowconfigure(row, weight=1)
            
        self.title_label = ctk.CTkLabel(self, text=f"Grundinformationen {self.username}", **self.styles["subtitle"])
        self.title_label.grid(row=0, columnspan=4, sticky="nsew")
        
        self.start_date_label = ctk.CTkLabel(self, text=f"Startdatum: ", **self.styles["text"])
        self.start_date_label.grid(row=1, column= 0, padx=10, pady=10, sticky="nsew")
        
        self.hours_per_day_label = ctk.CTkLabel(self, text=f"Stunden pro Tag: ", **self.styles["text"])
        self.hours_per_day_label.grid(row=1, column= 1, padx=10, pady=10, sticky="nsew")
        
        self.employment_percentage_label = ctk.CTkLabel(self, text=f"Stellenprozent: ", **self.styles["text"])
        self.employment_percentage_label.grid(row=1, column= 2, padx=10, pady=10, sticky="nsew")
        
        self.vacation_hours_label = ctk.CTkLabel(self, text=f"Ferientage: ", **self.styles["text"])
        self.vacation_hours_label.grid(row=1, column= 3, padx=10, pady=10, sticky="nsew")
    
    def load_user_settings(self):
        if not self.user_id:
            messagebox.showerror("Fehler", "Keine Benutzer-ID angegeben.")
            return
        
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                query = """
                SELECT default_hours_per_day, employment_percentage, vacation_hours, start_date
                FROM user_settings
                WHERE user_id = %s
                """
                cursor.execute(query, (self.user_id,))
                result = cursor.fetchone()
                
                if result:
                    self.default_hours_per_day = result[0]
                    self.employment_percentage = result[1]
                    self.vacation_days = float(result[2])/float(result[0])
                    self.start_date = result[3]
                    
                    self.start_date_label.configure(text=f"Startdatum: {self.start_date}")
                    self.hours_per_day_label.configure(text=f"Stunden pro Tag: {self.default_hours_per_day}")
                    self.employment_percentage_label.configure(text=f"Stellenprozent: {self.employment_percentage}")
                    self.vacation_hours_label.configure(text=f"Ferientage: {self.vacation_days}")
            except Exception as e:
                messagebox.showerror("Fehler", str(e))
            finally:
                cursor.close()
                connection.close()