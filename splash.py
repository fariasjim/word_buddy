import sys
from PyQt6.QtWidgets import (QApplication, QSplashScreen, QMainWindow, QLabel)
from PyQt6.QtGui import QPixmap, QMovie
from PyQt6.QtCore import Qt, QSize, QTimer
import os
import requests
import zipfile
import io
import shutil
import time
import Main
from tkinter import messagebox
import subprocess

# Configuration for update
REPO_OWNER = "fariasjim"
REPO_NAME = "wordbuddy"
BRANCH = "main"
ZIP_URL = f"https://github.com/{REPO_OWNER}/{REPO_NAME}/archive/refs/heads/{BRANCH}.zip"

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_EXTRACT_DIR = os.path.join(CURRENT_DIR, "temp_update")

url = "https://raw.githubusercontent.com/fariasjim/wordbuddy/refs/heads/main/version.txt"
url1 = "https://raw.githubusercontent.com/fariasjim/wordbuddy/refs/heads/main/update.bat"
# --- [MainWindow and DynamicGifSplashScreen classes remain the same as the previous response] ---
# ... (Assuming the fixed classes from the previous step are here)
version = "1.0.2[3]\n"

HIDE_WINDOW_FLAG = 0x08000000 

def run_batch_file_hidden(batch_file_path):
    """
    Executes a Windows batch file without showing the command-line window.
    """
    if sys.platform != "win32":
        print("This function is only applicable to Windows systems.")
        return

    # 1. Define the command to run the batch file
    # 'cmd /c' executes the command and then terminates the command shell.
    command = ["cmd.exe", "/c", batch_file_path]

    try:
        # 2. Use subprocess.Popen and set the creationflags argument
        subprocess.Popen(
            command,
            creationflags=HIDE_WINDOW_FLAG,
            shell=False,
            # Redirect stdout/stderr so the main script doesn't block waiting 
            # for output that might never come if the batch script hangs.
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print(f"Started batch file '{batch_file_path}' silently.")
        
    except FileNotFoundError:
        print(f"Error: Batch file not found at {batch_file_path}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if getattr(sys, 'frozen', False):
    # If running as a PyInstaller bundle
    base_path = sys._MEIPASS
else:
    base_path = os.path.abspath(os.path.dirname(__file__))

image_path1 = os.path.join(base_path, 'assets', 'WordBuddy(load).gif')
image_path2 = os.path.join(base_path, 'assets', 'WordBuddy.gif')
image_path3 = os.path.join(base_path, 'assets', 'WordBuddy2.gif')
image_path4 = os.path.join(base_path, 'assets', 'WordBuddy3.gif')
global response
response = requests.get(url)
print("got response")
print(response.text)
batch_file_path = os.path.join(base_path, "update.bat")

# Re-pasting the core fixed splash screen for completeness:
class DynamicGifSplashScreen(QSplashScreen):
    def __init__(self, initial_movie_path):
        super().__init__(QPixmap())  
        self.setWindowFlags(
            Qt.WindowType.SplashScreen | 
            Qt.WindowType.FramelessWindowHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.movie_label = QLabel(self) 
        self.movie_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.movie = QMovie(initial_movie_path)
        self.movie_label.setMovie(self.movie) 

        self.movie.frameChanged.connect(self._adjust_size_to_movie)
        self.movie.start() 
        
    def _adjust_size_to_movie(self):
        movie_size = self.movie.currentPixmap().size()
        if movie_size.isNull(): return
        
        self.resize(movie_size)
        self.movie_label.resize(movie_size) 

        new_pixmap = QPixmap(movie_size)
        new_pixmap.fill(Qt.GlobalColor.transparent)
        self.setPixmap(new_pixmap)

        try:
            self.movie.frameChanged.disconnect(self._adjust_size_to_movie)
        except TypeError:
            pass
            
    def update_gif(self, new_gif_path):
        self.movie.stop()
        self.movie.setFileName(new_gif_path)
        self.movie.frameChanged.connect(self._adjust_size_to_movie)
        self.movie.start()
        self.repaint()


# --- 3. New Loading Manager Class ---

class LoadingManager():
    def __init__(self, splash, main_window_class):
        self.splash = splash
        self.main_window_class = main_window_class
        
        # Define the loading stages (GIF path, delay in milliseconds)
        self.stages = [
            (image_path1, 300),  # 2 seconds
            (image_path2, 3280),  # 2 seconds
            (image_path3, 100),  # 2 seconds
            (image_path4, 100), # 1 second
        ]
        self.current_stage = 0
        self.start_loading()

    def start_loading(self):
        """Kicks off the first stage."""
        print(f"Starting stage {self.current_stage + 1}: {self.stages[self.current_stage][0]}")
        
        # The first GIF is already set in __init__, so we just wait
        self._set_next_stage_timer()

    def _set_next_stage_timer(self):
        """Sets a timer to trigger the next stage after the delay."""
        if self.current_stage < len(self.stages):
            delay_ms = self.stages[self.current_stage][1]
            
            # Use QTimer.singleShot to wait NON-BLOCKINGLY
            QTimer.singleShot(delay_ms, self.advance_loading)

        else:
            self.finish_loading()

    def advance_loading(self):
        """Triggers the next GIF change and timer."""
        self.current_stage += 1
        global response
        print(response.text)
        if self.current_stage <= 2:
            next_gif, _ = self.stages[self.current_stage]
            
            # COMMAND: Update the GIF while the event loop is running!
            self.splash.update_gif(next_gif)
            print(f"Advancing to stage {self.current_stage + 1}: {next_gif}")
            
            self._set_next_stage_timer()
        
        elif self.current_stage == 3:
            next_gif, _ = self.stages[self.current_stage]
            print("On Loading Phase.. You can code here i guess")
            if batch_file_path:
                try:
                    os.remove(batch_file_path)
                except Exception as e:
                    pass
            if response.status_code == 200:
                print("fetching version")
                if response.text == version:
                    Main.main()
                    Main.app.mainloop()
                    splash.close()
                elif response.text == "4000\n":
                    messagebox.showerror("Under maintenance", "Update under progress/Author has ended software support")
                    app.processEvents()
                    splash.close()
                else:
                    self.splash.update_gif(next_gif)
                    self._set_next_stage_timer()                 
            else:
                messagebox.showerror("Error", "Failed to check for Validation")
                sys.exit()
        else:
            #response = requests.get(url1, stream=True)
            #response.raise_for_status()  # Raise error if download fails
            #with open(batch_file_path, "wb") as f:
            #    for chunk in response.iter_content(chunk_size=8192):
            #        f.write(chunk)
            #run_batch_file_hidden("update.bat")
            messagebox.showinfo("Update Available","New update available. Press OK to update and restart")
            sys.exit()

    def finish_loading(self):
        """Initializes and shows the main application window."""
        print("Loading complete! Showing main window.")
        self.main_window = self.main_window_class()
        self.splash.finish(self.main_window)
        self.main_window.show()


# --- 4. Main Execution Block (Simplified) ---

def main():
    app = QApplication(sys.argv)
    
    # 🚨 Ensure all three GIF files exist in the script directory
    splash = DynamicGifSplashScreen(image_path1)
    splash.show()
    app.processEvents() 
    
    # Start the loading process managed by the QTimer
    manager = LoadingManager(splash, app)
    
    # The application loop stays running, allowing the QTimer and QMovie to work
    sys.exit(app.exec())

if __name__ == "__main__":
    main()