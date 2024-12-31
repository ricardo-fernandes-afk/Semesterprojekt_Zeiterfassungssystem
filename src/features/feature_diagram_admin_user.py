import customtkinter as ctk
import calendar
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from db.db_connection import create_connection
from gui.gui_appearance_color import appearance_color, get_default_styles

class AdminUserDiagram(ctk.CTkFrame):
    def __init__(self, master, user_id, filter_frame=None):
        self.colors = appearance_color()
        self.styles = get_default_styles()
        super().__init__(master, corner_radius=10, fg_color=self.colors["background_light"])
        self.user_id = user_id
        self.filter_frame = filter_frame