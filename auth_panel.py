import customtkinter
from CTkToolTip import CTkToolTip
import devinfo
import uuid

uuid = str(uuid.getnode())


class tab_pane(customtkinter.CTkTabview):
    def __init__(self, master=None):
        super().__init__(master, width=300, height=300, corner_radius=20)
        self._segmented_button.configure(
            corner_radius=20, font=("monofur Nerd Font", 20)
        )
        login_page = self.add("Login 󰍂 ")
        signup_page = self.add("SignUp  ")
        self.add_widgets(login_page, panel_id="login")
        self.add_widgets(signup_page, panel_id="signup")

    def add_widgets(self, panel_name, panel_id):
        self.u_name = customtkinter.CTkEntry(
            panel_name,
            placeholder_text="USERNAME...",
            corner_radius=20,
            font=("monofur Nerd Font", 20),
            width=260,
            height=40,
        )
        self.u_name.grid(row=0, column=0, padx=20, pady=10)
        self.passwd = customtkinter.CTkEntry(
            panel_name,
            placeholder_text="PASSWORD...",
            show="*",
            corner_radius=20,
            font=("monofur Nerd Font", 20),
            width=260,
            height=40,
        )
        self.passwd.grid(row=1, column=0, padx=20, pady=10)
        if panel_id == "login":
            self.remember_me = customtkinter.CTkCheckBox(
                panel_name, text="Remember me", font=("monofur Nerd Font", 20)
            )
            self.remember_me.grid(row=2, column=0, padx=20, pady=10, sticky="w")
            self.login_button = customtkinter.CTkButton(
                panel_name,
                text="Login 󰍂 ",
                font=("monofur Nerd Font", 20),
                width=260,
                height=40,
                corner_radius=20,
            )
            self.login_button.grid(row=3, column=0, padx=20, pady=20)
        elif panel_id == "signup":
            self.license_input = customtkinter.CTkEntry(
                panel_name,
                placeholder_text="LICENSE",
                corner_radius=20,
                font=("monofur Nerd Font", 20),
                width=260,
                height=40,
            )
            CTkToolTip(
                self.license_input,
                message="""If there is no license, then keep it blank.
Demo license will be generated with 7 days validity""",
                delay=0.3,
                font=("monofur Nerd Font", 12),
                corner_radius=20,
            )
            self.license_input.grid(row=2, column=0, padx=20, pady=10, sticky="w")
            self.signup_button = customtkinter.CTkButton(
                panel_name,
                text="SignUp  ",
                font=("monofur Nerd Font", 20),
                width=260,
                height=40,
                corner_radius=20,
            )
            self.signup_button.grid(row=3, column=0, padx=20, pady=10)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Login/SignUp | WordBuddy")
        self.geometry("500x630")
        self.resizable(False, False)
        self.heading = customtkinter.CTkLabel(
            self, text="WordBuddy", font=("monofur Nerd Font", 50, "bold")
        )
        self.heading.place(relx=0.28, rely=0.08)
        self.view = tab_pane(master=self)
        self.view.place(relx=0.18, rely=0.2)
        self.contact_button = customtkinter.CTkButton(
            self,
            text="Support  ",
            command=lambda: devinfo.credit_window(self),
            font=("monofur Nerd Font", 20),
        )
        self.contact_button.place(relx=0.68, rely=0.927)
        self.machine_number = customtkinter.CTkLabel(
            self, text=f"  Machine ID- {uuid}", font=("monofur Nerd Font", 20)
        )
        self.machine_number.place(relx=0.02, rely=0.927)
        self.protocol("WM_DELETE_WINDOW", self.onClosing)

    def onClosing(self, *args):
        self.destroy()
        import sys

        sys.exit()  # Kills the Python process


app = App()
app.mainloop()
