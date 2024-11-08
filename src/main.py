import customtkinter as ctk
from gui_appearance_color import appearance_color
from gui_login import LoginGUI


def main():
    
    # Hauptfenster des Programms
    appearance_color()
    
    # Starte das Login Interface
    root = ctk.CTk()
    login_gui = LoginGUI(master=root)
    root.mainloop() 
    
if __name__ == "__main__":
    main()