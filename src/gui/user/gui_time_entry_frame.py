import customtkinter as ctk
from tkinter import messagebox
from features.feature_save_time_entry import save_hours
from db.db_connection import create_connection
from gui.gui_appearance_color import appearance_color, get_default_styles

class TimeEntryFrame(ctk.CTkFrame):
    def __init__(self, master):
        self.colors=appearance_color()
        self.styles=get_default_styles()
        
        super().__init__(master, corner_radius=10, fg_color=self.colors["alt_background"])
        self.selected_date = None
        self.create_widgets()
        
    def create_widgets(self):
        
        time_entry_frame = ctk.CTkFrame(self, fg_color=self.colors["alt_background"])
        time_entry_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Label für das Datum
        self.date_label = ctk.CTkLabel(time_entry_frame, text="Datum: --", **self.styles["small_text"])
        self.date_label.pack(padx=10, pady=10, side="top")

        # Eingabefeld für Stunden
        self.hours_entry = ctk.CTkEntry(time_entry_frame, placeholder_text="Stunden eingeben", **self.styles["entry"])
        self.hours_entry.pack(padx=10)
        
        # Dropdown für die Aktivität
        if self.master.selected_project_number == "0000":
            activity_options = ["IT Arbeiten", "Besprechung", "Büroadmin", "Event", "Absenz", "Ferien", "Allgemeines", "Acquisition"]
        else:
            activity_options = ["Planung", "Besprechung", "Korrespondenz", "Bauadmin", "Bauleitung", "Verkauf"]
        
        self.activity_dropdown = ctk.CTkComboBox(time_entry_frame, values=activity_options, **self.styles["combobox"])
        self.activity_dropdown.set(activity_options[0])
        self.activity_dropdown.pack(padx=10, pady=10)
        
        # Notizfeld
        self.notes_entry = ctk.CTkEntry(time_entry_frame, placeholder_text="Notizen", **self.styles["entry"])
        self.notes_entry.pack(padx=10)
        
        # Label für die Stunden an diesem Tag
        self.phase_hours_label = ctk.CTkLabel(time_entry_frame, text="", justify="left", **self.styles["text"])
        self.phase_hours_label.pack(padx=10, pady=10)
        
        # Label für die Gesamtstunden an diesem Tag
        self.total_hours_label = ctk.CTkLabel(time_entry_frame, text="", justify="left", font=("Arial", 14, "bold"))
        self.total_hours_label.pack(padx=10, pady=(0,10))
        
        # Button zum Speichern
        save_button = ctk.CTkButton(
            time_entry_frame,
            text="Speichern",
            command=self.save_time_entry,
            **self.styles["button"],
        )
        save_button.pack()
        
        # Button zum Löschen der Stunden
        self.delete_button = ctk.CTkButton(
            time_entry_frame,
            text="Löschen",
            command=self.delete_time_entry,
            fg_color=self.colors["error"],
            hover_color=self.colors["warning"],
        )
        self.delete_button.pack(pady=10, side="bottom")        

    def update_date(self, selected_date):
        self.selected_date = selected_date
        self.date_label.configure(text=f"Datum: {selected_date}")
        self.load_hours()
        
    def load_hours(self):
        """Lädt vorhandene Stunden für das ausgewählte Datum aus der Datenbank."""
        if not self.selected_date:
            return

        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                phase_query = """
                SELECT te.project_number, COALESCE (s.phase_name, '') AS phase_name, te.activity, te.hours
                FROM time_entries te
                LEFT JOIN sia_phases s ON te.phase_id = s.phase_id
                WHERE te.user_id = %s AND te.entry_date = %s
                """
                cursor.execute(phase_query, (self.master.user_id, self.selected_date))
                results = cursor.fetchall()
                
                # Abfrage für die Gesamtstunden
                total_hours_query = """
                SELECT COALESCE(SUM(te.hours), 0)
                FROM time_entries te
                WHERE te.user_id = %s AND te.entry_date = %s
                """
                cursor.execute(total_hours_query, (self.master.user_id, self.selected_date))
                total_hours = cursor.fetchone()[0]
                
                phase_hours_text = ""
                if results:
                    # Erstellen eines Texts mit allen Phasenstunden
                    for result in results:
                        project_number = result[0]
                        phase_name = result[1]
                        activity = result[2]
                        hours = result[3]
                        phase_hours_text += f"{project_number}: {phase_name}    {activity}   {hours}h\n"
                else:
                    phase_hours_text += "Keine Stunden an diesem Tag.\n"

                # Anzeige des Texts im Label
                self.phase_hours_label.configure(text=phase_hours_text)
                self.total_hours_label.configure(text=f"Gesamtstunden:  {total_hours:.2f}h")

            except Exception as e:
                print(f"Fehler beim Laden der Stunden: {e}")
            finally:
                cursor.close()
                connection.close()
        
    def delete_time_entry(self):
        """Löscht die eingetragenen Stunden für das ausgewählte Datum aus der Datenbank."""
        if not self.selected_date:
            messagebox.showerror("Fehler", "Kein Datum ausgewählt.")
            return
        
        confirm = messagebox.askyesno("Löschen bestätigen", "Bist du sicher, dass du die Stunden für diesen Tag löschen möchtest?")
        if not confirm:
            return

        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                # Löschen der Stunden für den ausgewählten Tag
                delete_query = """
                DELETE FROM time_entries
                WHERE user_id = %s AND project_number = %s AND entry_date = %s
                """
                cursor.execute(delete_query, (self.master.user_id, self.master.selected_project_number, self.selected_date))
                connection.commit()
                messagebox.showinfo("Erfolgreich", f"Stunden für {self.master.selected_project_number} am {self.selected_date} erfolgreich gelöscht.")
                
                # Eingabefeld und Label nach dem Löschen zurücksetzen
                self.hours_entry.configure(state="normal")
                self.hours_entry.delete(0, "end")
                self.phase_hours_label.configure(text="")
                self.total_hours_label.configure(text="")

            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim Löschen der Stunden: {e}")
            finally:
                cursor.close()
                connection.close()
        self.load_hours()

    def save_time_entry(self):
        hours = self.hours_entry.get()
        activity = self.activity_dropdown.get()
        note = self.notes_entry.get() if self.notes_entry.get() else None
        
        if not hours or not activity or not self.selected_date:
            messagebox.showerror("Fehler", "Datum, Stunden, Phase oder Tätigkeit fehlen.")
            return
        
        phase_id = None

        user_id = self.master.user_id
        project_number = self.master.selected_project_number
        
        # Überprüfung der Phase für normale Projekte
        if project_number != "0000":  # Normales Projekt
            if hasattr(self.master, "choose_sia_phase_frame") and hasattr(self.master.choose_sia_phase_frame, "selected_phase_id"):
                phase_id = self.master.choose_sia_phase_frame.selected_phase_id
            if not phase_id:  # Wenn keine Phase ausgewählt wurde
                messagebox.showerror("Fehler", "Bitte wählen Sie eine SIA Phase aus.")
                return
                
        print(f"DEBUG: Stunden={hours}, Tätigkeit={activity}, Notiz={note}, Datum={self.selected_date}, PhaseID={phase_id}")
        print(f"DEBUG: Benutzer-ID={user_id}, Projekt-ID={project_number}, Phase-ID={phase_id}")

        success = save_hours(user_id, project_number, phase_id, hours, self.selected_date, activity, note)
        if success:
            messagebox.showinfo("Erfolgreich", f"Stunden für {self.selected_date} erfolgreich gespeichert.")
            self.hours_entry.delete(0, "end")
            self.notes_entry.delete(0, "end")
            self.load_hours()
        else:
            messagebox.showerror("Fehler", f"Fehler beim Speichern der Stunden für {self.selected_date}.")
            
        
