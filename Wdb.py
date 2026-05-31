import sys
from PyQt6.QtWidgets import QApplication, QSplashScreen, QMainWindow, QLabel
from PyQt6.QtGui import QPixmap, QMovie
from PyQt6.QtCore import Qt, QTimer
import os
import requests
import Main
from tkinter import messagebox
import subprocess

# Configuration for update
REPO_OWNER = "fariasjim"
REPO_NAME = "word_buddy"
BRANCH = "main"
ZIP_URL = f"https://github.com/{REPO_OWNER}/{REPO_NAME}/archive/refs/heads/{BRANCH}.zip"
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_EXTRACT_DIR = os.path.join(CURRENT_DIR, "temp_update")
url = (
    "https://raw.githubusercontent.com/fariasjim/word_buddy/refs/heads/main/version.txt"
)
url1 = (
    "https://raw.githubusercontent.com/fariasjim/word_buddy/refs/heads/main/update.bat"
)
version = "1.1[3]\n"
HIDE_WINDOW_FLAG = 0x08000000


def run_batch_file_hidden(batch_file_path):
    if sys.platform != "win32":
        messagebox.showerror(
            "Error", "This function is only applicable to Windows systems."
        )
        return
    command = ["cmd.exe", "/c", batch_file_path]
    try:
        subprocess.Popen(
            command,
            creationflags=HIDE_WINDOW_FLAG,
            shell=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except FileNotFoundError as e:
        messagebox.showerror("Error", "Batch file not found at {batch_file_path}")
    except Exception as e:
        messagebox.showerror("Error", "An unexpected error occurred: {e}")


if getattr(sys, "frozen", False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.abspath(os.path.dirname(__file__))
image_path1 = os.path.join(base_path, "assets", "WordBuddy(load).gif")
image_path2 = os.path.join(base_path, "assets", "WordBuddy.gif")
image_path3 = os.path.join(base_path, "assets", "WordBuddy2.gif")
image_path4 = os.path.join(base_path, "assets", "WordBuddy3.gif")
global response
response = requests.get(url)
batch_file_path = os.path.join(base_path, "update.bat")


class DynamicGifSplashScreen(QSplashScreen):
    def __init__(self, initial_movie_path):
        super().__init__(QPixmap())
        self.setWindowFlags(
            Qt.WindowType.SplashScreen | Qt.WindowType.FramelessWindowHint
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
        if movie_size.isNull():
            return
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


class LoadingManager:
    def __init__(self, splash, main_window_class):
        self.splash = splash
        self.main_window_class = main_window_class
        self.stages = [
            (image_path1, 300),
            (image_path2, 3280),
            (image_path3, 2000),
            (image_path4, 100),
        ]
        self.current_stage = 0
        self.start_loading()

    def start_loading(self):
        self._set_next_stage_timer()

    def _set_next_stage_timer(self):
        if self.current_stage < len(self.stages):
            delay_ms = self.stages[self.current_stage][1]
            QTimer.singleShot(delay_ms, self.advance_loading)

    def advance_loading(self):
        self.current_stage += 1
        global response
        if self.current_stage <= 2:
            next_gif, _ = self.stages[self.current_stage]
            self.splash.update_gif(next_gif)
            self._set_next_stage_timer()
        elif self.current_stage == 3:
            next_gif, _ = self.stages[self.current_stage]
            if batch_file_path:
                try:
                    os.remove(batch_file_path)
                except Exception as e:
                    pass
            if response.status_code == 200:
                if response.text == version:
                    Main.main()
                    self.splash.destroy()
                    Main.app.mainloop()
                elif response.text < version:
                    messagebox.showinfo(
                        "Under Development Version",
                        "You are using an under development version. Please Report any error found to author.",
                    )
                    self.splash.destroy()
                    Main.app.mainloop()
                elif response.text == "4000\n":
                    messagebox.showerror(
                        "Under maintenance",
                        "Update under progress/Author has ended software support",
                    )
                    self.splash.destroy()
                else:
                    self.splash.update_gif(next_gif)
                    self._set_next_stage_timer()
            else:
                messagebox.showerror("Error", "Failed to check for Validation")
                sys.exit()
        else:
            response = requests.get(url1, stream=True)
            response.raise_for_status()  # Raise error if download fails
            with open(batch_file_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            run_batch_file_hidden("update.bat")


def main():
    app = QApplication(sys.argv)
    splash = DynamicGifSplashScreen(image_path1)
    splash.show()
    app.processEvents()
    manager = LoadingManager(splash, app)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
