import customtkinter as ctk
from gui.user.gui_choose_sia_phase_frame import ChooseSIAPhaseFrame
from gui.user.gui_calendar_frame import CalendarFrame
from gui.user.gui_time_entry_frame import TimeEntryFrame

class UserSelectedFrame(ctk.CTkFrame):
    def __init__(self, master, user_id, selected_id=None, selected_name=None, description=None):
        super().__init__(master, corner_radius=10)
        self.user_id = user_id
        self.selected_id = selected_id
        self.selected_name = selected_name
        self.description = description
        self.time_entry_frame = None
        self.selected_project_number = None
        self.create_widgets()
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=2)
        self.grid_rowconfigure(4, weight=2)
        for col in range(2):
            self.grid_columnconfigure(col, weight=1)
    
    def clear_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()

    def create_widgets(self):
        self.title_label = self.create_title_label()
        self.description_label = self.create_description_label()

    def create_title_label(self):
        title_text = f"{self.selected_id} {self.selected_name}" if self.selected_name else "Wählen Sie ein Projekt"
        title_label = ctk.CTkLabel(self, text=title_text, font=("", 18, "bold"))
        title_label.grid(row=0, columnspan=2, pady=5, sticky="nsew")
        return title_label

    def create_description_label(self):
        description_label = ctk.CTkLabel(self, text="", font=("", 16), wraplength=300)
        description_label.grid(row=1, columnspan=2, sticky="nsew")
        return description_label

    def update_project_details(self, selected_id, selected_name, description=None):
        self.clear_widgets()
        self.create_widgets()       
        self.selected_id = selected_id
        self.selected_name = selected_name
        self.description = description
        self.selected_project_number = selected_id
        
        self.title_label.configure(text=f"{selected_id} - {selected_name}")
        self.description_label.configure(text=self.description) 
        
        self.choose_sia_phase_frame = ChooseSIAPhaseFrame(self, project_number=self.selected_id)
        self.choose_sia_phase_frame.grid(row=2, columnspan=2, padx=10, pady=10, sticky="nsew")
        
        self.calendar_frame = CalendarFrame(self, stunden_uebersicht_frame=self)
        self.calendar_frame.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
        self.calendar_frame.on_date_selected(None)
        
        self.time_entry_frame = TimeEntryFrame(self)
        self.time_entry_frame.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")
        
        self.diagram_frame = ctk.CTkFrame(self)
        self.diagram_frame.grid(row=4, columnspan=2, padx=10, pady=10, sticky="nsew")
        
    def update_date(self, selected_date):
        if self.time_entry_frame:
            self.time_entry_frame.update_date(selected_date)

