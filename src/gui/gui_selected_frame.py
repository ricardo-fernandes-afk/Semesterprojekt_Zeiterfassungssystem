import customtkinter as ctk
from gui.gui_sia_phasen_soll_stunden_frame import SIAPhasenSollStundenFrame

class SelectedFrame(ctk.CTkFrame):
    def __init__(self, master, selected_id=None, selected_name=None, description=None):
        super().__init__(master, corner_radius=10)
        self.selected_id = selected_id
        self.selected_name = selected_name
        self.description = description
        self.soll_stunden_entries = {}
        self.sia_phases_frame = None
        self.create_widgets()

    def clear_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()

    def create_widgets(self):
        self.title_label = self.create_title_label()
        self.description_label = self.create_description_label()

    def create_title_label(self):
        title_text = f"{self.selected_id} {self.selected_name}" if self.selected_name else "Wählen Sie ein Projekt oder einen Benutzer"
        title_label = ctk.CTkLabel(self, text=title_text, font=("", 18, "bold"))
        title_label.pack(pady=10)
        return title_label

    def create_description_label(self):
        description_label = ctk.CTkLabel(self, text="", font=("", 16), wraplength=300)
        description_label.pack()
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

            self.sia_phases_frame = SIAPhasenSollStundenFrame(self)
            self.sia_phases_frame.pack(pady=5, anchor="n", fill="x", expand=True)
        else:
            self.title_label.configure(text=f"{selected_name}")
            self.description_label.configure(text="")
            if self.sia_phases_frame is not None:
                self.sia_phases_frame.destroy()
