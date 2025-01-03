"""
Modul: Benutzergrundinformationen für TimeArch.

Dieses Modul stellt eine grafische Benutzeroberfläche (GUI) bereit, um die Grundinformationen eines Benutzers
anzuzeigen und zu bearbeiten. Es unterstützt die Speicherung von Einstellungen wie Arbeitsstunden pro Tag,
Beschäftigungsprozentsatz, Ferientagen und Startdatum.

Klassen:
--------
- GrundInfosUser: Hauptklasse für die Anzeige und Bearbeitung der Benutzergrundinformationen.

Methoden:
---------
- __init__(self, master, user_id=None): Initialisiert das Grundinformationen-Frame mit dem übergeordneten Fenster und Benutzer-ID.
- create_widgets(self): Erstellt die Widgets für die Anzeige und Bearbeitung der Benutzergrundinformationen.
- save_user_settings(self): Speichert die aktualisierten Benutzerinformationen in der Datenbank.
- load_user_settings(self): Lädt die Benutzerinformationen aus der Datenbank.
- toggle_entries(self, state="normal"): Aktiviert oder deaktiviert die Eingabefelder.
- edit_user_settings(self): Aktiviert die Bearbeitung der Benutzerinformationen.

Verwendung:
-----------
    from gui_grundinfos_user import GrundInfosUser

    frame = GrundInfosUser(master, user_id=1)
    frame.pack()
"""

import customtkinter as ctk
from datetime import date
from tkinter import messagebox
from db.db_connection import create_connection
from gui.gui_appearance_color import appearance_color, get_default_styles

class GrundInfosUser(ctk.CTkFrame):
    """
    Eine Klasse, die eine grafische Oberfläche zur Verwaltung der Benutzergrundinformationen bereitstellt.

    Ermöglicht das Anzeigen und Bearbeiten von:
    - Arbeitsstunden pro Tag
    - Beschäftigungsprozentsatz
    - Ferientagen
    - Startdatum
    """
    def __init__(self, master, user_id=None):
        """
        Initialisiert die Benutzergrundinformationen-GUI.

        Args:
            master (ctk.CTk): Das übergeordnete Fenster.
            user_id (int, optional): Die Benutzer-ID, deren Informationen geladen werden sollen. Standard ist None.
        """
        self.colors = appearance_color()
        self.styles = get_default_styles()
        super().__init__(master, corner_radius=10, fg_color=self.colors["alt_background"])
        
        self.user_id = user_id
        self.create_widgets()
        if self.user_id:
            self.load_user_settings()   # Vorhandene Daten laden oder Standardwerte setzen
        
    def create_widgets(self):
        """
        Erstellt die Widgets zur Anzeige und Bearbeitung der Benutzergrundinformationen.

        - Enthält Eingabefelder für Startdatum, Arbeitsstunden, Stellenprozent und Ferientage.
        - Fügt Schaltflächen für Speichern und Bearbeiten hinzu.
        """
        self.title_label = ctk.CTkLabel(self, text="Grundinformationen", **self.styles["subtitle"])
        self.title_label.pack(padx=10, pady=(10,0))
        
        eingabe_frame = ctk.CTkFrame(self, fg_color=self.colors["alt_background"])
        eingabe_frame.pack(padx=10, fill="x")
        
        for col in range(4):
            eingabe_frame.grid_columnconfigure(col, weight=1)
        
        # Startdatum
        self.start_date_label = ctk.CTkLabel(eingabe_frame, text="Startdatum", **self.styles["text"])
        self.start_date_label.grid(row=0, column=0, padx=10, sticky="s")
        self.start_date_entry = ctk.CTkEntry(eingabe_frame, placeholder_text="YYYY-MM-DD", **self.styles["entry"])
        self.start_date_entry.grid(row=1, column=0, padx=10)
        
        # Stunden pro Tag
        self.hours_label = ctk.CTkLabel(eingabe_frame, text="Stunden pro Tag", **self.styles["text"])
        self.hours_label.grid(row=0, column=1, padx=10, sticky="s")
        self.hours_entry = ctk.CTkEntry(eingabe_frame, placeholder_text="8.5", **self.styles["entry"])
        self.hours_entry.grid(row=1, column=1, padx=10)
        
        # Stellenprozent
        self.percentage_label = ctk.CTkLabel(eingabe_frame, text="Stellenprozent", **self.styles["text"])
        self.percentage_label.grid(row=0, column=2, padx=10, sticky="s")
        self.percentage_entry = ctk.CTkEntry(eingabe_frame, placeholder_text="100", **self.styles["entry"])
        self.percentage_entry.grid(row=1, column=2, padx=10)
        
        # Ferientage
        self.vacation_label = ctk.CTkLabel(eingabe_frame, text="Ferientage", **self.styles["text"])
        self.vacation_label.grid(row=0, column=3, padx=10, sticky="s")
        self.vacation_entry = ctk.CTkEntry(eingabe_frame, placeholder_text="20", **self.styles["entry"])
        self.vacation_entry.grid(row=1, column=3, padx=10)
        
        button_frame = ctk.CTkFrame(eingabe_frame, fg_color=self.colors["alt_background"])
        button_frame.grid(row=2, columnspan=4, padx=10, pady=10)
        
        # Speichern_Button
        self.save_button = ctk.CTkButton(
            button_frame,
            text="Speichern",
            command=self.save_user_settings,
            **self.styles["button"],
        )
        self.save_button.pack(side="left", padx=10)
        
        # Bearbeiten_Button
        self.edit_button = ctk.CTkButton(
            button_frame,
            text="Bearbeiten",
            command=self.edit_user_settings,
            **self.styles["button_secondary"],
        )
        self.edit_button.pack(side="right", padx=10)
    
    def save_user_settings(self):
        """
        Speichert die Benutzerinformationen in der Datenbank.

        - Aktualisiert oder fügt neue Einträge in der Tabelle `user_settings` hinzu.
        - Berechnet Ferientage in Stunden und speichert sie entsprechend.
        - Zeigt eine Erfolgsmeldung bei erfolgreichem Speichern an.

        Fehlerbehandlung:
        ------------------
        - Zeigt eine Fehlermeldung an, falls ein Fehler bei der Datenbankabfrage auftritt.
        """
        default_hours = self.hours_entry.get() or 8.5
        percentage = self.percentage_entry.get() or 100
        vacation_days = self.vacation_entry.get() or 20
        vacation_hours = float(vacation_days) * float(default_hours)
        start_date = self.start_date_entry.get() or date(date.today().year, 1, 1)
        
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                check_query = "SELECT COUNT (*) FROM user_settings WHERE user_id = %s"
                cursor.execute(check_query, (self.user_id,))
                exists = cursor.fetchone()[0] > 0
                if exists:
                    update_query = """
                    UPDATE user_settings
                    SET default_hours_per_day = %s,
                        employment_percentage = %s,
                        vacation_hours = %s,
                        start_date = %s
                    WHERE user_id = %s
                    """
                    cursor.execute(update_query, (default_hours, percentage, vacation_hours, start_date, self.user_id))
                else:
                    insert_query = """
                    INSERT INTO user_settings (user_id, default_hours_per_day, employment_percentage, vacation_hours, start_date)
                    VALUES (%s, %s, %s, %s, %s)
                    """
                    cursor.execute(insert_query, (self.user_id, default_hours, percentage, vacation_hours, start_date))
                    
                connection.commit()
                self.toggle_entries(state="normal")
                messagebox.showinfo("Erfolg", "Einstellungen wurden gespeichert.")
            except Exception as e:
                messagebox.showerror("Fehler", str(e))
            finally:
                cursor.close()
                connection.close()
        self.toggle_entries(state="disabled")
        if self.master.diagram_frame:
            self.master.diagram_frame.update_chart()
    
    def load_user_settings(self):
        """
        Lädt die Benutzerinformationen aus der Datenbank und zeigt sie in den Eingabefeldern an.

        - Ruft Daten aus der Tabelle `user_settings` ab.
        - Zeigt Standardwerte an, wenn keine Informationen in der Datenbank gefunden werden.

        Fehlerbehandlung:
        ------------------
        - Zeigt eine Fehlermeldung an, falls ein Fehler bei der Datenbankabfrage auftritt.
        """
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
                print(f"Result: {result}")

                if result:
                    start_date = result[3]
                    # Daten aus der Datenbank anzeigen
                    self.start_date_entry.insert(0, start_date.strftime("%Y-%m-%d"))
                    self.hours_entry.insert(0, str(result[0]))
                    self.percentage_entry.insert(0, str(result[1]))
                    vacation_days = float(result[2]) / float(result[0])  # Stunden in Tage umrechnen
                    self.vacation_entry.insert(0, str(vacation_days))
                else:
                    # Standardwerte anzeigen
                    self.start_date_entry.insert(0, date(date.today().year, 1, 1).strftime("%Y-%m-%d"))
                    self.hours_entry.insert(0, "8.5")
                    self.percentage_entry.insert(0, "100")
                    self.vacation_entry.insert(0, "20")
            except Exception as e:
                messagebox.showerror("Fehler", str(e))
            finally:
                cursor.close()
                connection.close()
        self.toggle_entries(state="disabled")
    
    def toggle_entries(self, state="normal"):
        """
        Aktiviert oder deaktiviert die Eingabefelder.

        Args:
            state (str): Der Zustand der Eingabefelder. Standard ist "normal".
        """
        self.start_date_entry.configure(state=state)
        self.hours_entry.configure(state=state)
        self.percentage_entry.configure(state=state)
        self.vacation_entry.configure(state=state)
    
    def edit_user_settings(self):
        """
        Aktiviert die Bearbeitung der Benutzerinformationen.

        - Schaltet die Eingabefelder in den Bearbeitungsmodus.
        """
        self.toggle_entries(state="normal")
        self.is_editable = True

