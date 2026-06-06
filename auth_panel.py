import customtkinter
import devinfo
import uuid

uuid = str(uuid.getnode())


class tab_pane(customtkinter.CTkTabview):
    def __init__(self, master=None, corner_radius=50):
        super().__init__(master, width=300, height=300)
        self._segmented_button.configure(
            corner_radius=20, font=("monofur Nerd Font", 20)
        )
        login_page = self.add("Login 󰍂 ")
        signup_page = self.add("SignUp  ")
        self.add_widgets(login_page, panel_id="login")

    def add_widgets(self, panel_name, panel_id):
        self.u_name = customtkinter.CTkEntry(
            panel_name,
            placeholder_text="USERNAME...",
            corner_radius=20,
            font=("monofur Nerd Font", 20),
            width=260,
            height=40,
        )
        self.u_name.place(relx=0.05, rely=0.1)
        self.passwd = customtkinter.CTkEntry(
            panel_name,
            placeholder_text="PASSWORD",
            show="*",
            corner_radius=20,
            font=("monofur Nerd Font", 20),
            width=260,
            height=40,
        )
        self.passwd.place(relx=0.05, rely=0.4)
        if panel_id == "login":
            self.remember_me = customtkinter.CTkCheckBox(
                panel_name, text="Remember me", font=("monofur Nerd Font", 20)
            )
            self.remember_me.place(relx=0.05, rely=0.7)
            self.login_button = customtkinter.CTkButton(
                panel_name,
                text="Login 󰍂 ",
                font=("monofur Nerd Font", 20),
                width=260,
                height=40,
                corner_radius=20,
            )
            self.login_button.place(relx=0.05, rely=0.9)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Login/SignUp | WordBuddy")
        self.geometry("500x630")
        self.resizable(False, False)
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


app = App()
app.mainloop()
