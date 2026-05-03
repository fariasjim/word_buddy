import customtkinter as ctk
import sys
import os
from PIL import Image


def resource_path(relative_path):
    """Get absolute path to resource (for PyInstaller or normal run)"""
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS  # PyInstaller temp folder
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


global img3
img1 = resource_path("assets/1.png")
img2 = resource_path("assets/2.png")
icon = resource_path("assets/3.ico")
img3 = resource_path("assets/4.png")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("WordBuddy")
        self.image1 = ctk.CTkImage(
            light_image=Image.open(img2), dark_image=Image.open(img1), size=(400, 600)
        )
        self.image1.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")


app = App()
try:
    app.iconbitmap(icon)  # Set the icon for the application
except:
    pass
if __name__ == "__main__":
    app.mainloop()

