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

# 🔧 Config
REPO_OWNER = "fariasjim"
REPO_NAME = "wordbuddy"
BRANCH = "main"
ZIP_URL = f"https://github.com/{REPO_OWNER}/{REPO_NAME}/archive/refs/heads/{BRANCH}.zip"

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_EXTRACT_DIR = os.path.join(CURRENT_DIR, "temp_update")

def download_repo_zip():
    response = requests.get(ZIP_URL)
    if response.status_code == 200:
        return response.content
    else:
        messagebox.showerror("Error","Update Error")

def extract_zip(content):
    with zipfile.ZipFile(io.BytesIO(content)) as zip_ref:
        if os.path.exists(TEMP_EXTRACT_DIR):
            shutil.rmtree(TEMP_EXTRACT_DIR)
        zip_ref.extractall(TEMP_EXTRACT_DIR)

def overwrite_current_directory():
    extracted_subfolder = os.path.join(TEMP_EXTRACT_DIR, f"{REPO_NAME}-{BRANCH}")
    
    for item in os.listdir(extracted_subfolder):
        src = os.path.join(extracted_subfolder, item)
        dst = os.path.join(CURRENT_DIR, item)

        if os.path.exists(dst):
            if os.path.isdir(dst):
                shutil.rmtree(dst)
            else:
                os.remove(dst)

        if os.path.isdir(src):
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)

def restart_script():
    time.sleep(1)
    os.execl(sys.executable, sys.executable, *sys.argv)

def main():
    zip_content = download_repo_zip()
    extract_zip(zip_content)
    overwrite_current_directory()
    shutil.rmtree(TEMP_EXTRACT_DIR)

    # Optional: restart
    restart_script()

url = "https://raw.githubusercontent.com/fariasjim/wordbuddy/refs/heads/main/version.txt"
response = requests.get(url)

version = "1.0.0\n"  # Current version of your application

if response.status_code == 200:
    if response.text == version:
        Main.app.mainloop()  # Start the main application loop
    else:
        messagebox.showinfo("Update Available","New update available. Press OK to update and restart")
        main()
        
        
    
else:
    messagebox.showerror("Error","Can't get version Info. No Internet ?")
