import customtkinter
from CTkToolTip import CTkToolTip
import devinfo
import auth
from tkinter import messagebox
import time

uid = auth.generate_stable_machine_uid()
uuid = uid[0:14]


class tab_pane(customtkinter.CTkTabview):
    def __init__(self, master=None):
        super().__init__(master, width=300, height=300, corner_radius=20)
        self._segmented_button.configure(
            corner_radius=20, font=("monofur Nerd Font", 20)
        )
        self.login_page = self.add("Login 󰍂 ")
        self.signup_page = self.add("SignUp  ")
        self.add_widgets()
        self.is_loading = False

    def on_login(self):
        if len(self.u_name_l.get()) == 0:
            messagebox.showerror("Error", "Please Input Username")
            return
        if len(self.passwd_l.get()) < 8 or len(self.passwd_l.get()) > 12:
            messagebox.showerror(
                "Error", "Password should be between 8 and 12 characters long."
            )
            return
        self.is_loading = True
        self.login_button.configure(state="disabled")
        self.u_name_l.configure(state="disabled")
        self.passwd_l.configure(state="disabled")
        self.animate_login_button(1)

    def animate_login_button(self, step):
        if not self.is_loading:
            return
        if step == 1:
            self.login_button.configure(text="Logging in.")
            next_step = 2
        elif step == 2:
            self.login_button.configure(text="Logging in..")
            next_step = 3
        elif step == 3:
            self.login_button.configure(text="Logging in...")
            next_step = 1

        self.login_button.after(500, self.animate_login_button, next_step)

    def add_widgets(self):
        self.u_name_l = customtkinter.CTkEntry(
            self.login_page,
            placeholder_text="USERNAME...",
            corner_radius=20,
            font=("monofur Nerd Font", 20),
            width=260,
            height=40,
        )
        self.u_name_l.grid(row=0, column=0, padx=20, pady=10)
        self.passwd_l = customtkinter.CTkEntry(
            self.login_page,
            placeholder_text="PASSWORD...",
            show="*",
            corner_radius=20,
            font=("monofur Nerd Font", 20),
            width=260,
            height=40,
        )
        self.passwd_l.grid(row=1, column=0, padx=20, pady=10)
        self.remember_me = customtkinter.CTkCheckBox(
            self.login_page, text="Remember me", font=("monofur Nerd Font", 20)
        )
        self.remember_me.grid(row=2, column=0, padx=20, pady=10, sticky="w")
        self.login_button = customtkinter.CTkButton(
            self.login_page,
            text="Login 󰍂 ",
            font=("monofur Nerd Font", 20),
            width=260,
            height=40,
            corner_radius=20,
            command=self.on_login,
        )
        self.login_button.grid(row=3, column=0, padx=20, pady=20)
        self.u_name_s = customtkinter.CTkEntry(
            self.signup_page,
            placeholder_text="USERNAME...",
            corner_radius=20,
            font=("monofur Nerd Font", 20),
            width=260,
            height=40,
        )
        self.u_name_s.grid(row=0, column=0, padx=20, pady=10)
        self.passwd_s = customtkinter.CTkEntry(
            self.signup_page,
            placeholder_text="PASSWORD...",
            show="*",
            corner_radius=20,
            font=("monofur Nerd Font", 20),
            width=260,
            height=40,
        )
        self.passwd_s.grid(row=1, column=0, padx=20, pady=10)
        self.license_input = customtkinter.CTkEntry(
            self.signup_page,
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
            self.signup_page,
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
            self, text=f"  {uuid.strip()}", font=("monofur Nerd Font", 20)
        )
        self.machine_number.place(relx=0.02, rely=0.927)
        self.protocol("WM_DELETE_WINDOW", self.onClosing)

    def onClosing(self, *args):
        self.destroy()
        import sys

        sys.exit()  # Kills the Python process


app = App()
app.mainloop()
