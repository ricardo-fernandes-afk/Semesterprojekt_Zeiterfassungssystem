import customtkinter as ctk
from db.db_connection import create_connection
from gui.gui_appearance_color import appearance_color, get_default_styles

class GrundInfosUser(ctk.CTkFrame):
    def __init__(self, master, user_id=None):
        self.colors = appearance_color()
        self.styles = get_default_styles()
        super().__init__(master, corner_radius=10, fg_color=self.colors["alt_background"])
        
        self.user_id = user_id
        self.create_widgets()
        
    def create_widgets(self):
        
        self.title_label = ctk.CTkLabel(self, text="Grundinformationen", **self.styles["subtitle"])
        self.title_label.pack(padx=10, pady=(10,0))
        
        eingabe_frame = ctk.CTkFrame(self, fg_color=self.colors["alt_background"])
        eingabe_frame.pack(padx=10, pady=10, fill="x")
        
        for col in range(3):
            eingabe_frame.grid_columnconfigure(col, weight=1)
        
        # Stunden pro Tag
        self.hours_label = ctk.CTkLabel(eingabe_frame, text="Stunden pro Tag", **self.styles["text"])
        self.hours_label.grid(row=0, column=0, padx=10, sticky="s")
        self.hours_entry = ctk.CTkEntry(eingabe_frame, placeholder_text="8.5", **self.styles["entry"])
        self.hours_entry.grid(row=1, column=0, padx=10)
        
        # Stellenprozent
        self.percentage_label = ctk.CTkLabel(eingabe_frame, text="Stellenprozent", **self.styles["text"])
        self.percentage_label.grid(row=0, column=1, padx=10, sticky="s")
        self.percentage_entry = ctk.CTkEntry(eingabe_frame, placeholder_text="100", **self.styles["entry"])
        self.percentage_entry.grid(row=1, column=1, padx=10)
        
        # Ferientage
        self.vacation_label = ctk.CTkLabel(eingabe_frame, text="Ferientage", **self.styles["text"])
        self.vacation_label.grid(row=0, column=2, padx=10, sticky="s")
        self.vacation_entry = ctk.CTkEntry(eingabe_frame, placeholder_text="20", **self.styles["entry"])
        self.vacation_entry.grid(row=1, column=2, padx=10)
        
        # Speichern_Button
        self.save_button = ctk.CTkButton(eingabe_frame, text="Speichern", command=self.save_user_settings, **self.styles["button"])
        self.save_button.grid(row=2, columnspan=3, padx=10, pady=10)
    
    def save_user_settings(self):
        default_hours = self.hours_entry.get()
        percentage = self.percentage_entry.get()
        vacation_days = self.vacation_entry.get()
        vacation_hours = float(vacation_days) * float(default_hours)
        
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                query = """
                UPDATE users
                SET default_hours_per_day = %s,
                employment_percentage = %s,
                vacation_hours = %s
                WHERE user_id = %s
                """
                cursor.execute(query, (default_hours, percentage, vacation_hours, self.user_id))
                connection.commit()
                ctk.CTkMessagebox.showinfo("Erfolg", "Einstellungen wurden gespeichert.")
            except Exception as e:
                ctk.CTkMessagebox.showerror("Fehler", str(e))
            finally:
                cursor.close()
                connection.close()
