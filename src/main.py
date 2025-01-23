"""
Modul: Hauptprogramm für TimeArch.

Dieses Modul ist der Einstiegspunkt für die Anwendung. Es startet die Login-GUI und initialisiert das Hauptfenster für die Benutzerinteraktion.

Funktionen:
-----------
- main(): Startet die Login-GUI und verwaltet die Ereignisschleife.

Verwendung:
-----------
    python main.py
"""

import customtkinter as ctk
from gui.gui_login import LoginGUI

def main():
    """
    Startet das Hauptprogramm.

    - Initialisiert das Hauptfenster mit der Login-GUI.
    - Verwaltet die Ereignisschleife (mainloop) der Anwendung.
    - Beendet das Programm bei einer KeyboardInterrupt-Ausnahme.

    Fehlerbehandlung:
    ------------------
    - Gibt eine Meldung aus, wenn das Programm durch eine Tastatureingabe beendet wird.
    """
    root = ctk.CTk()
    login_gui = LoginGUI(master=root)
    try:
        root.mainloop() 
    except KeyboardInterrupt:
        print("Programm beendet.")
    
if __name__ == "__main__":
    main()