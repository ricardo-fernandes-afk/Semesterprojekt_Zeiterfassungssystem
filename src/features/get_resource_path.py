import os
import sys
import customtkinter as ctk

# Pfad zum aktuellen Skript (funktioniert auch nach PyInstaller)
def get_resource_path(relative_path):
    """ Gibt den Pfad zur Datei zurück, auch wenn das Programm als .exe ausgeführt wird. """
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

icon_path = get_resource_path("src/Logo_TimeArch.ico")