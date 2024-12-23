import customtkinter as ctk
from gui.admin.gui_sia_phasen_soll_stunden_frame import SIAPhasenSollStundenFrame
from gui.admin.gui_user_to_project_frame import UserToProjectFrame
from gui.admin.gui_stunden_uebersicht_project import StundenUebersichtProjectFrame
from gui.admin.gui_grundinfos_user import GrundinfosUser
from gui.admin.gui_stunden_uebersicht_user import StundenUebersichtUserFrame
from gui.gui_appearance_color import appearance_color, get_default_styles

class SelectedFrame(ctk.CTkFrame):
    def __init__(self, master, user_id=None, selected_id=None, selected_name=None, description=None):
        self.colors = appearance_color()
        self.styles = get_default_styles()
        
        super().__init__(master, corner_radius=10, fg_color=self.colors["background"])
        self.user_id = user_id
        self.selected_id = selected_id
        self.selected_name = selected_name
        self.description = description
        self.soll_stunden_entries = {}
        self.sia_phases_frame = None
        self.user_to_project_frame = None
        self.create_widgets()
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=3)
        self.grid_rowconfigure(4, weight=2)
        for col in range(0,4):
            self.grid_columnconfigure(col, weight=1)
            

    def clear_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()

    def create_widgets(self):
        self.title_label = self.create_title_label()
        self.description_label = self.create_description_label()

    def create_title_label(self):
        title_text = f"{self.selected_id} {self.selected_name}" if self.selected_name else "Wählen Sie ein Projekt oder einen Benutzer"
        title_label = ctk.CTkLabel(self, text=title_text, **self.styles["title"])
        title_label.grid(row=0, columnspan=4, pady=5, sticky="nsew")
        return title_label

    def create_description_label(self):
        description_label = ctk.CTkLabel(self, text="", **self.styles["description"], wraplength=500)
        description_label.grid(row=1, columnspan=4, sticky="nsew")
        return description_label

    def update_project_details(self, selected_id, selected_name, description=None):
        self.clear_widgets()
        self.create_widgets()
        
        self.selected_id = selected_id
        self.selected_name = selected_name
        self.description = description        

        self.title_label.configure(text=f"{selected_id} - {selected_name}")
        self.description_label.configure(text=self.description if self.description else "")

        self.sia_phases_frame = SIAPhasenSollStundenFrame(self, project_number=selected_id)
        self.sia_phases_frame.grid(row=2, columnspan=4, padx=10, pady=10, sticky="nsew")
        
        self.user_to_project_frame = UserToProjectFrame(self, project_number=selected_id)
        self.user_to_project_frame.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
        
        self.stunden_uebersicht_project_frame = StundenUebersichtProjectFrame(self, project_number=selected_id)
        self.stunden_uebersicht_project_frame.grid(row=3, column=1, columnspan=3, padx=10, pady=10, sticky="nsew")
        
        self.diagram_frame = ctk.CTkFrame(self)
        self.diagram_frame.grid(row=4, columnspan=4, padx=10, pady=10, sticky="nsew")

    def update_user_details(self, selected_user_id, selected_username):
        self.clear_widgets()
        self.create_widgets()

        self.selected_id = selected_user_id
        self.selected_name = selected_username

        self.title_label.configure(text=f"{selected_username}")
        self.description_label.configure(text="")

        self.grundinfos_user_frame = GrundinfosUser(self)
        self.grundinfos_user_frame.grid(row=2, columnspan=4, padx=10, pady=10, sticky="nsew")

        self.stunden_uebersicht_user_frame = StundenUebersichtUserFrame(self, user_id=selected_user_id)
        self.stunden_uebersicht_user_frame.grid(row=3, columnspan=4, padx=10, pady=10, sticky="nsew")

        self.diagram_frame = ctk.CTkFrame(self)
        self.diagram_frame.grid(row=4, columnspan=4, padx=10, pady=10, sticky="nsew")
            
            
