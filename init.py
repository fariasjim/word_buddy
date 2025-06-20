import requests
import Main
import customtkinter as ctk
from tkinter import messagebox
import os
import sys
import zipfile
import io
import shutil
import time

# Config
REPO_OWNER = "fariasjim"
REPO_NAME = "wordbuddy"
BRANCH = "main"
ZIP_URL = f"https://github.com/{REPO_OWNER}/{REPO_NAME}/archive/refs/heads/{BRANCH}.zip"

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_EXTRACT_DIR = os.path.join(CURRENT_DIR, "temp_update")

url = "https://raw.githubusercontent.com/fariasjim/wordbuddy/refs/heads/main/version.txt"
response = requests.get(url)

version = "1.0.1\n"  # Current version of application

print(response.text)
if response.status_code == 200:
    if response.text == version:
        Main.main()
        Main.app.mainloop()  # Start the main application loop
    elif response.text == "4000\n":
        messagebox.showerror("Under maintenance", "Update under progress/Author has ended software support")
    else:
        messagebox.showinfo("Update Available","New update available. Press OK to update and restart")
        os.startfile("update.bat")
        
    
else:
    messagebox.showerror("Error","Can't get version Info. No Internet ?")
