import customtkinter

class frame(customtkinter.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.place(relx=0.5, rely=0.5)
        self.text = customtkinter.CTkLabel(self, text="Howdy")
        self.

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Login/SignUp | WordBuddy")
        self.geometry("500x630")
        self.resizable(False, False)


app = App()
app.mainloop()
