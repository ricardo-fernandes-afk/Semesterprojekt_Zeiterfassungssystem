import customtkinter as ctk
from features.feature_save_time_entry import save_hours
from db.db_connection import create_connection

class TimeEntryFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=10)
        self.selected_date = None
        self.create_widgets()

    def create_widgets(self):
        
        time_entry_frame = ctk.CTkFrame(self)
        time_entry_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Label für das Datum
        self.date_label = ctk.CTkLabel(time_entry_frame, text="Datum: --", font=("", 14, "bold"))
        self.date_label.pack(padx=10, pady=(10, 0), side="top")

        # Eingabefeld für Stunden
        self.hours_entry = ctk.CTkEntry(time_entry_frame, placeholder_text="Stunden eingeben")
        self.hours_entry.pack(padx=10, pady=10, anchor="center")

        # Button zum Speichern
        save_button = ctk.CTkButton(time_entry_frame, text="Speichern", command=self.save_time_entry)
        save_button.pack(pady=(0,10), side="bottom")

    def update_date(self, selected_date):
        self.selected_date = selected_date
        self.date_label.configure(text=f"Datum: {selected_date}")
        self.load_hours()
        
    def load_hours(self):
        """Lädt vorhandene Stunden für das ausgewählte Datum aus der Datenbank."""
        if not self.selected_date or not self.master.selected_project_number or not self.master.choose_sia_phase_frame.selected_phase_id:
            return

        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                query = """
                SELECT hours FROM time_entries
                WHERE user_id = %s AND project_number = %s AND phase_id = %s AND entry_date = %s
                """
                cursor.execute(query, (
                    self.master.user_id,
                    self.master.selected_project_number,
                    self.master.choose_sia_phase_frame.selected_phase_id,
                    self.selected_date
                ))
                result = cursor.fetchone()
                if result:
                    self.hours_entry.delete(0, "end")
                    self.hours_entry.insert(0, str(result[0]))
                else:
                    self.hours_entry.delete(0, "end")
            finally:
                cursor.close()
                connection.close()

    def save_time_entry(self):
        hours = self.hours_entry.get()
        
        print(f"user_id: {self.master.user_id}")
        print(f"project_number: {self.master.selected_project_number}")
        print(f"phase_id: {self.master.choose_sia_phase_frame.selected_phase_id}")
        print(f"hours: {hours}")
        print(f"entry_date: {self.selected_date}")
        
        if not hours or not self.selected_date:
            print("Fehler: Datum oder Stunden fehlen.")
            return

        user_id = self.master.user_id
        project_number = self.master.selected_project_number
        phase_id = self.master.choose_sia_phase_frame.selected_phase_id

        success = save_hours(user_id, project_number, phase_id, hours, self.selected_date)
        if success:
            print(f"Stunden für {self.selected_date} erfolgreich gespeichert.")
            self.hours_entry.delete(0, "end")
        else:
            print(f"Fehler beim Speichern der Stunden für {self.selected_date}.")
        
        print(f"Nach Aktualisierung - project_number: {self.master.selected_project_number}")
