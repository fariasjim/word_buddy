import customtkinter
from PIL import Image
import os
import sys


def resource_path(relative_path):
    """Get absolute path to resource (for PyInstaller or normal run)"""
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS  # PyInstaller temp folder
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


dev_img_black = resource_path("assets/dev(Black).png")
dev_img_white = resource_path("assets/dev(White).png")
nerd_font = resource_path("assets/Monofur.ttf")
customtkinter.FontManager.load_font(nerd_font)


def open_url(which):
    import webbrowser

    if which == "report":
        webbrowser.open(
            "https://docs.google.com/forms/d/e/1FAIpQLSfD0Z7ZIF7GLmJNEENhhN6mvwvYRv8xapLqLLxOmXO8drRizQ/viewform?usp=sharing&ouid=112908537690851176933"
        )
    elif which == "facebook":
        webbrowser.open("https://www.facebook.com/jimmy.hthc")
    elif which == "whatsapp":
        webbrowser.open("https://wa.me/+8801624245116")
    elif which == "git":
        webbrowser.open("https://github.com/fariasjim/word_buddy")
    elif which == "github":
        webbrowser.open("https://github.com/fariasjim")


class credit_window(customtkinter.CTkToplevel):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.geometry("920x450")
        self.title("About the dev")
        self.resizable(False, False)
        self.devi_label = customtkinter.CTkLabel(
            self,
            text=" Dev Info",
            font=("monofur Nerd Font", 50),
            anchor="w",
            justify="left",
        )
        self.devi_label.grid(
            row=0, column=0, columnspan=4, padx=20, pady=20, sticky="nsew"
        )
        self.name_label = customtkinter.CTkLabel(
            self,
            text=r"""
___________            .__                      ____.__         
\_     _____/____ _______|__|____    ______     |    |__| _____  
 |    __) \__  \\_  __ \  \__  \  /  ___/      |    |  |/     \ 
 |     \   / __ \|  | \/  |/ __ \_\___ \   /\__|    |  |  Y Y  \
 \___  /  (____  /__|  |__(____  /____  >  \________|__|__|_|  /
     \/        \/              \/     \/                    \/ 
""",
            font=("Courier New", 10, "bold"),
        )
        self.name_label.grid(
            row=1, column=0, columnspan=4, padx=20, pady=20, sticky="w"
        )
        self.my_image = customtkinter.CTkImage(
            light_image=Image.open(dev_img_white),
            dark_image=Image.open(dev_img_black),
            size=(300, 300),
        )
        self.image_label = customtkinter.CTkLabel(self, image=self.my_image, text="")
        self.image_label.grid(row=1, rowspan=3, column=4, sticky="w")
        self.info_label = customtkinter.CTkLabel(
            self,
            text=r"""===============================================
[Role]       Software Engineer / Automation Dev
[Location]   Dhaka, Bangladesh
[Core Tech]  Python, Java, Linux

"Building tools to automate the boring stuff"
===============================================""",
            font=("Courier New", 20),
            anchor="w",
            justify="left",
        )
        self.info_label.grid(row=2, columnspan=4, padx=20, column=0)
        self.report_button = customtkinter.CTkButton(
            self,
            text="  Report Issues",
            font=("monofur Nerd Font", 20),
            hover=True,
            hover_color="Red",
            command=lambda: open_url(which="report"),
        )
        self.report_button.grid(row=0, column=4, sticky="e")
        self.fb_label = customtkinter.CTkLabel(
            self, text=" ", font=("monofur Nerd Font", 40), anchor="w", justify="left"
        )
        self.fb_label.grid(row=3, column=0, padx=30, pady=10, sticky="w")
        self.fb_label.bind(
            "<Enter>", lambda e: self.fb_label.configure(text_color="#2979ff")
        )
        self.fb_label.bind("<Button-1>", lambda e: open_url(which="facebook"))
        self.fb_label.bind(
            "<Leave>", lambda e: self.fb_label.configure(text_color="Black")
        )
        self.wa_label = customtkinter.CTkLabel(
            self, text=" ", font=("monofur Nerd Font", 40), anchor="w", justify="left"
        )
        self.wa_label.grid(row=3, column=1, padx=30, pady=10, sticky="w")
        self.wa_label.bind("<Button-1>", lambda e: open_url(which="whatsapp"))
        self.wa_label.bind(
            "<Enter>", lambda e: self.wa_label.configure(text_color="#25D366")
        )
        self.wa_label.bind(
            "<Leave>", lambda e: self.wa_label.configure(text_color="Black")
        )
        self.git_label = customtkinter.CTkLabel(
            self, text="󰊢 ", font=("monofur Nerd Font", 40), anchor="w", justify="left"
        )
        self.git_label.grid(row=3, column=2, padx=30, pady=10, sticky="w")
        self.git_label.bind("<Button-1>", lambda e: open_url(which="git"))
        self.git_label.bind(
            "<Enter>", lambda e: self.git_label.configure(text_color="#F05032")
        )
        self.git_label.bind(
            "<Leave>", lambda e: self.git_label.configure(text_color="Black")
        )
        self.gh_label = customtkinter.CTkLabel(
            self, text=" ", font=("monofur Nerd Font", 40), anchor="w", justify="left"
        )
        self.gh_label.grid(row=3, column=3, padx=30, pady=10, sticky="w")
        self.gh_label.bind("<Button-1>", lambda e: open_url(which="github"))
        self.gh_label.bind(
            "<Enter>", lambda e: self.gh_label.configure(text_color="#181717")
        )
        self.gh_label.bind(
            "<Leave>", lambda e: self.gh_label.configure(text_color="Black")
        )


if __name__ == "__main__":
    # Create the required main application root first
    app = customtkinter.CTk()
    app.geometry("300x200")

    # # Button to open our Toplevel window
    # btn = customtkinter.CTkButton(
    #     app, text="Open Window", command=lambda: credit_window(app)
    # )
    hello = credit_window(app)
    # btn.pack(pady=50)

    app.mainloop()
