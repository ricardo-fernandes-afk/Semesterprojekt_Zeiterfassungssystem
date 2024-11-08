import customtkinter as ctk
from gui_login import create_login_layout


def main():
    
    # Hauptfenster des Programms
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")
    
    # Starte das Login Interface
    create_login_layout()
    
if __name__ == "__main__":
    main()