import sys
import time
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QSplashScreen, QMainWindow
import requests
import Main
import customtkinter as ctk
from tkinter import messagebox
import os
import zipfile
import io
import shutil
import time


# Configuration for update
REPO_OWNER = "fariasjim"
REPO_NAME = "wordbuddy"
BRANCH = "main"
ZIP_URL = f"https://github.com/{REPO_OWNER}/{REPO_NAME}/archive/refs/heads/{BRANCH}.zip"

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_EXTRACT_DIR = os.path.join(CURRENT_DIR, "temp_update")

url = "https://raw.githubusercontent.com/fariasjim/wordbuddy/refs/heads/main/version.txt"

version = "1.0.2\n"  # Current version of application

app = QApplication(sys.argv)

# Load a pixmap (image) for your splash screen
if getattr(sys, 'frozen', False):
    # If running as a PyInstaller bundle
    base_path = sys._MEIPASS
else:
    base_path = os.path.abspath(os.path.dirname(__file__))

image_path = os.path.join(base_path, 'assets', 'Wordbuddy_splash.png')
pixmap = QPixmap(image_path)  # Use absolute path for compatibility with PyInstaller

# Create the splash screen object
splash = QSplashScreen(pixmap, Qt.WindowType.WindowStaysOnTopHint)
splash.show()
app.processEvents()
splash.showMessage(
    "Checking for updates...", 
    alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter, 
    color=Qt.GlobalColor.white)
app.processEvents()
time.sleep(0.5)  # Simulate a delay for checking updates
response = requests.get(url)
if response.status_code == 200:
    if response.text == version:  # Start the main application loop
        splash.showMessage(
            "Loading Wordbuddy...", 
            alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter, 
            color=Qt.GlobalColor.white
        )
        app.processEvents()
        time.sleep(0.5)  # Simulate a delay for loading
        splash.close()
        Main.main()
        Main.app.mainloop()
    elif response.text == "4000\n":
        splash.showMessage(
            "Update under progress/Author has ended software support", 
            alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter, 
            color=Qt.GlobalColor.red
        )
        messagebox.showerror("Under maintenance", "Update under progress/Author has ended software support")
        app.processEvents()
        time.sleep(3)  # Simulate a delay for loading
        splash.close()
    else:
        splash.showMessage(
            "Update available!!!!!", 
            alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter, 
            color=Qt.GlobalColor.blue
        )
        app.processEvents()
        time.sleep(3)  # Simulate a delay for loading
        splash.close()
        messagebox.showinfo("Update Available","New update available. Press OK to update and restart")
        os.startfile("update.bat")


# Simulate your app loading (replace with actual loading code)
###time.sleep(3)  # Simulate a delay for loading

# Main application window
##main_win = QMainWindow()
##main_win.setWindowTitle("Wordbuddy")
##main_win.resize(800, 600)
##main_win.show()

# Close splash screen and start the main app
##splash.finish(main_win)

###sys.exit(app.exec())