"""
Modul: Benutzer-Frame für TimeArch.

Dieses Modul stellt die grafische Benutzeroberfläche bereit, um Benutzer zu verwalten. Es umfasst Funktionen zum Hinzufügen, Löschen und Anzeigen von Benutzern in einer Tabelle.

Klassen:
--------
- UserFrame: Hauptklasse für die Verwaltung der Benutzer.

Methoden:
---------
- __init__(self, master): Initialisiert den Benutzer-Frame und erstellt die Widgets.
- get_selected_user(self): Gibt die ID und den Benutzernamen des ausgewählten Benutzers zurück.
- load_users(self): Lädt die Benutzer aus der Datenbank und zeigt sie in der Tabelle an.
- open_add_user_window(self): Öffnet ein Fenster zum Hinzufügen eines neuen Benutzers.
- open_delete_user_window(self): Öffnet ein Bestätigungsfenster zum Löschen eines Benutzers.

Verwendung:
-----------
    from gui_users_frame import UserFrame

    frame = UserFrame(master)
    frame.pack()
"""

import customtkinter as ctk
from tkinter import messagebox, ttk
from db.db_connection import create_connection
from features.feature_add_users import add_user
from features.feature_delete_users import delete_user, get_selected_user_id
from gui.gui_appearance_color import appearance_color, get_default_styles, apply_treeview_style

class UserFrame(ctk.CTkFrame):
    """
    Eine Klasse, die die Benutzerverwaltung ermöglicht.

    Funktionen:
    - Benutzer anzeigen
    - Benutzer hinzufügen
    - Benutzer löschen
    """
    def __init__(self, master):
        """
        Initialisiert den Benutzer-Frame.

        Args:
            master (ctk.CTk): Das übergeordnete Fenster.
        """
        self.colors = appearance_color()
        self.styles = get_default_styles()
        
        super().__init__(master, corner_radius=10, fg_color=self.colors["background"])
        self.grid_propagate(False)
        
        # Label für Users
        user_label = ctk.CTkLabel(master=self, text="Benutzer", **self.styles["title"])
        user_label.pack(pady=10, anchor="n")
        
        # Liste der Users
        tree_frame = ctk.CTkFrame(master=self, fg_color=self.colors["alt_background"])
        tree_frame.pack(padx=10, fill="both", expand=True)
        
        columns = ("ID", "Username", "Password", "Role")
        self.user_treeview = ttk.Treeview(tree_frame, columns=columns, show="headings")
        apply_treeview_style(self.colors)
        
        self.update_idletasks()
        frame_width = self.winfo_width()
        
        num_columns = len(columns)
        if frame_width > 0:
            column_width = frame_width // num_columns
        else:
            column_width = 100
        
        for col in columns:
            self.user_treeview.heading(col, text=col)
            self.user_treeview.column(col, minwidth=50, width=column_width, stretch=True)
            
        self.user_treeview.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        # Scrollbar hinzufügen
        scrollbar = ctk.CTkScrollbar(
            tree_frame,
            command=self.user_treeview.yview,
            fg_color=self.colors["alt_background"],
            button_color=self.colors["background_light"],
        )
        self.user_treeview.configure(yscrollc=scrollbar.set)
        scrollbar.pack(side="right", fill="y", anchor="e")
        
        # Button zum Hinzufügen und Löschen von User
        add_button = ctk.CTkButton(
            self,
            text="Benutzer hinzufügen",
            command=self.open_add_user_window,
            **self.styles["button"]
        )
        add_button.pack(pady=10, anchor="s")
        
        delete_button = ctk.CTkButton(
            self,
            text="Benutzer löschen",
            command=self.open_delete_user_window,
            **self.styles["button_error"]
        )
        delete_button.pack(pady=10, anchor="s")
        
        self.load_users()
        
    def get_selected_user(self):
        """
        Gibt die ID und den Benutzernamen des ausgewählten Benutzers zurück.

        Returns:
            tuple: Ein Tupel bestehend aus der Benutzer-ID und dem Benutzernamen.
                   Gibt (None, None) zurück, wenn kein Benutzer ausgewählt ist.

        Fehlerbehandlung:
        ------------------
        - Gibt eine leere Auswahl zurück, falls keine Benutzerzeile markiert ist.
        """
        try:
            selected_item = self.user_treeview.selection()[0]  # Die ID des ausgewählten Elements abrufen
            user_values = self.user_treeview.item(selected_item, 'values')  # Die Werte des ausgewählten Benutzers abrufen
            if len(user_values) >= 1:
                return int(user_values[0]), user_values[1]  # `user_id` und `username` zurückgeben
            return None, None
        except IndexError:
            return None, None  # Keine Auswahl
        
    def load_users(self):
        """
        Lädt die Benutzer aus der Datenbank und zeigt sie in der Tabelle an.

        - Ruft die Benutzerinformationen (ID, Benutzername, Passwort, Rolle) aus der Datenbank ab.
        - Füllt das Treeview mit den abgerufenen Benutzerdaten.

        Fehlerbehandlung:
        ------------------
        - Zeigt eine Fehlermeldung an, falls die Datenbankabfrage fehlschlägt.
        """
        for item in self.user_treeview.get_children():
            self.user_treeview.delete(item)
            
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("SELECT user_id, username, password, role FROM users")
                users = cursor.fetchall()
                for user in users:
                    self.user_treeview.insert("", "end", values=(user[0], user[1], user[2], user[3]))
                    
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim Laden der Projekte {e}")
                
            finally:
                cursor.close()
                connection.close()
    
    def open_add_user_window(self):
        """
        Öffnet ein Fenster zum Hinzufügen eines neuen Benutzers.

        - Verwendet die Funktion `add_user` aus den Features.
        - Aktualisiert die Benutzerliste nach dem Hinzufügen.
        """
        add_user(self.master, self.load_users)
        
    def open_delete_user_window(self):
        """
        Öffnet ein Bestätigungsfenster zum Löschen eines Benutzers.

        - Verwendet die Funktion `delete_user` aus den Features.
        - Aktualisiert die Benutzerliste nach dem Löschen.
        - Zeigt eine Fehlermeldung an, wenn kein Benutzer ausgewählt ist.
        """
        user_id = get_selected_user_id(self.user_treeview)
        if user_id is None:
            messagebox.showerror("Fehler", "Bitte wählen Sie einen Benutzer aus")
            return
        
        confirmation = messagebox.askyesno("Bestätigung", "Sind Sie sicher, dass Sie diesen Benutzer löschen möchten?")
        if confirmation:
            delete_user(user_id, self.load_users)