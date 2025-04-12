import requests
import Main
import customtkinter as ctk
from tkinter import messagebox

url = "https://raw.githubusercontent.com/fariasjim/wordbuddy/refs/heads/main/version.txt"
response = requests.get(url)

version = "1.0.1\n"  # Current version of your application

if response.status_code == 200:
    if response.text == version:
        Main.app.mainloop()  # Start the main application loop
    else:
        messagebox.showinfo("Update", "You are using an older version. Auto Update is in progress")
        
    
else:
    print("Failed to fetch file.")
