import customtkinter as ctk
from tkinter import ttk

def appearance_color():
    # Farbschema definieren
    colors = {
        "primary": "#0F8100",       # Grün für Hauptaktionen
        "secondary": "#0010A2",     # Blau für unterstützende Aktionen
        "background": "#333333",    # Dunkler Hintergrund
        "alt_background": "#404040",  # Alternative für Container
        "background_light": "#F2F2F2",  # Heller Hintergrund
        "text_light": "#FFFFFF",    # Helle Schrift
        "text_dark": "#000000",     # Dunkle Schrift
        "error": "#B31200",         # Rot für Fehler
        "warning": "#5B0900",       # Gelb für Warnungen
        "hover": "#084800",         # Hover-Farbe
        "hover_secondary": "#00084E",  # Hover-Farbe für sekundäre Buttons
        "scrollbar": "#D3D3D3",     # Scrollbar-Farbe
        "disabled": "#A6A6A6"       # Deaktivierte Elemente
    }

    # Gibt das Farbschema zurück
    return colors


def apply_treeview_style(colors):
    colors = appearance_color()
    """Stil für Treeview-Elemente anwenden"""
    style = ttk.Style()
    style.theme_use("clam")  # Unterstützt mehr Farben
    style.configure("Treeview", 
                    background=colors["background_light"],
                    foreground=colors["text_dark"],
                    fieldbackground=colors["background_light"],
                    rowheight=25)
    style.configure("Treeview.Heading", 
                    background=colors["background_light"], 
                    foreground=colors["text_dark"], 
                    font=("Arial", 12, "bold"))
    style.map("Treeview", 
              background=[("selected", colors["text_light"])],
              foreground=[("selected", colors["text_dark"])])


def get_default_styles():
    colors = appearance_color()
    """Standardstile für häufige Elemente definieren"""
    return {
        "title": {"font": ("Arial", 22, "bold"), "text_color": colors["text_light"]},
        "description": {"font": ("Arial", 14, "italic"), "text_color": colors["text_light"]},
        "subtitle": {"font": ("Arial", 18, "bold"), "text_color": colors["text_light"]},
        "text": {"font": ("Arial", 14), "text_color": colors["text_light"]},
        "small_text": {"font": ("Arial", 10), "text_color": colors["text_light"]},
        "button": {"fg_color": colors["primary"], "hover_color": colors["hover"]},
        "button_secondary": {"fg_color": colors["secondary"], "hover_color": colors["hover_secondary"]},
        "button_error": {"fg_color": colors["error"], "hover_color": colors["warning"]},
        "entry": {"fg_color": colors["background_light"], "text_color": colors["text_dark"], "placeholder_text_color": colors["alt_background"]},
        "combobox": {"fg_color": colors["background_light"], "button_color": colors["primary"], "button_hover_color": colors["hover"], "text_color": colors["text_dark"]},
    }
