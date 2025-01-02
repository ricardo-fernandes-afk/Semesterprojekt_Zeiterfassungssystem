import customtkinter as ctk
from gui.gui_login import LoginGUI


def main():
    # Starte das Login Interface
    root = ctk.CTk()
    login_gui = LoginGUI(master=root)
    try:
        root.mainloop() 
    except KeyboardInterrupt:
        print("Programm beendet.")
    
if __name__ == "__main__":
    main()