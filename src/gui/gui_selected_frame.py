import customtkinter as ctk
from gui.gui_sia_phasen_soll_stunden_frame import SIAPhasenSollStundenFrame
from gui.gui_user_to_project import UserToProjectFrame

class SelectedFrame(ctk.CTkFrame):
    def __init__(self, master, selected_id=None, selected_name=None, description=None):
        super().__init__(master, corner_radius=10)
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
        self.grid_rowconfigure(4, weight=3)
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
        title_label = ctk.CTkLabel(self, text=title_text, font=("", 18, "bold"))
        title_label.grid(row=0, columnspan=4, sticky="nsew")
        return title_label

    def create_description_label(self):
        description_label = ctk.CTkLabel(self, text="", font=("", 16), wraplength=300)
        description_label.grid(row=1, columnspan=4, sticky="nsew")
        return description_label

    def update_project_details(self, selected_id, selected_name, description=None):
        self.clear_widgets()
        self.create_widgets()

        if selected_id is not None:
            self.selected_id = selected_id
            self.selected_name = selected_name
            self.description = description        

            self.title_label.configure(text=f"{selected_id} - {selected_name}")
            self.description_label.configure(text=self.description if self.description else "")

            self.sia_phases_frame = SIAPhasenSollStundenFrame(self, project_number=selected_id)
            self.sia_phases_frame.grid(row=2, columnspan=4, padx=10, pady=10, sticky="nsew")
            
            self.user_to_project_frame = UserToProjectFrame(self, selected_id)
            self.user_to_project_frame.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
            
            self.test_frame = ctk.CTkFrame(self)
            self.test_frame.grid(row=4, columnspan=4, padx=10, pady=10, sticky="nsew")
        else:
            self.title_label.configure(text=f"{selected_name}")
            self.description_label.configure(text="")
            if self.sia_phases_frame is not None:
                self.sia_phases_frame.destroy()
            if self.user_to_project_frame is not None:
                self.user_to_project_frame.destroy()
