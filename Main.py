import customtkinter
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox
from tkinter import colorchooser
import os
import convertion_logic  # Import the wordconv module
## fixing png loading problems
import sys
import json
import translation_logic


def resource_path(relative_path):
    """ Get absolute path to resource (for PyInstaller or normal run) """
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS  # PyInstaller temp folder
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

global img3
img1 = resource_path("assets/1.png")
img2 = resource_path("assets/2.png")
icon = resource_path("assets/3.ico")
img3 = resource_path("assets/4.png")


###Trying to add to path
import sys
import shutil
import ctypes
import subprocess

def is_admin():
    if os.name == 'nt':
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except:
            return False
    else:
        return os.geteuid() == 0

def is_script_in_path(script_path):
    paths = os.environ.get('PATH', '').split(os.pathsep)
    script_name = os.path.basename(script_path)
    for directory in paths:
        full_path = os.path.join(directory, script_name)
        if os.path.isfile(full_path):
            if os.path.samefile(script_path, full_path):
                return True
    return False

def install_script(script_path):
    paths = os.environ.get('PATH', '').split(os.pathsep)
    writable_paths = [p for p in paths if os.access(p, os.W_OK | os.X_OK)]
    if not writable_paths:
        sys.exit(1)
    target_dir = writable_paths[0]
    target_path = os.path.join(target_dir, os.path.basename(script_path))
    try:
        shutil.copy2(script_path, target_path)
        if os.name != 'nt':
            os.chmod(target_path, 0o755)
        return target_path
    except Exception as e:
        sys.exit(1)

def add_to_system_path_windows(new_path):
    current_path = os.environ.get('PATH', '')
    if new_path.lower() not in (p.lower() for p in current_path.split(';')):
        subprocess.run(f'setx PATH "{current_path};{new_path}"', shell=True)
        print(f"Added {new_path} to PATH.")

def main():
    script_path = os.path.abspath(sys.argv[0])
    if is_script_in_path(script_path):
        return
    
    if is_admin():
        new_path = install_script(script_path)
        # Optionally on Windows, add directory to system/user PATH
        if os.name == 'nt':
            add_to_system_path_windows(os.path.dirname(new_path))
            messagebox.showinfo(title="Added To Path", message="Now you can call the program from any Path.")
    else:
        pass

if __name__ == '__main__':
    main()



global file_path
global save_path
file_path = None
save_path = None
h_color = ""

class Translator(customtkinter.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)

        self.master = master
        self.label = customtkinter.CTkLabel(self, text="Text Translator", font=("Arial", 30, "bold"))
        self.label.grid(row=0, column=0, padx=20, pady=20)
        self.label2 = customtkinter.CTkLabel(self, text="Open Path", font=("Arial",20,"bold"))
        self.label2.grid(row=1, column=0, padx=20, sticky="w")

        self.button1 = customtkinter.CTkButton(self, text="Browse", command= code.open_path_code, width=100, corner_radius=20, hover= True, hover_color="gray")
        self.button1.grid(row=1, column=0, pady=5, sticky="e")

        self.label3 = customtkinter.CTkLabel(self, text="Save Path", font=("Arial",20,"bold"))
        self.label3.grid(row=2, column=0, padx=20, sticky="w")

        self.button2 = customtkinter.CTkButton(self, text="Browse", command= code.save_path_code, width=100, corner_radius=20, hover= True, hover_color="gray")
        self.button2.grid(row=2, column=0, pady=5, sticky="e")
        self.checkbox1 = customtkinter.CTkSwitch(self, text="Overwrite same file", variable=overwrite_value, font=("Arial",15,"bold"))
        self.checkbox1.grid(row=3, column=0, padx=20, pady=5, sticky="w")

        self.checkbox2 = customtkinter.CTkSwitch(self, text="Open file after translation", variable=open_after_work, font=("Arial",15,"bold"))
        self.checkbox2.grid(row=4, column=0, padx=20, pady=5, sticky="w")

        self.conv_button = customtkinter.CTkButton(self, text="TRANSLATE", font=("Bahnschrift SemiBold Condensed", 30), corner_radius=20, hover= True, hover_color="green", command=code.translate)
        self.conv_button.grid(row=9, column=0, pady=20)


class tabbed_frame(customtkinter.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.tabs = {}
        self.buttons = {}

        # Create tab bar and content area
        self.tab_bar = customtkinter.CTkFrame(self, fg_color="transparent")
        self.tab_bar.grid(row=0, column=0, sticky="ew")

        # Content frame where tab pages will be placed
        self.content = customtkinter.CTkFrame(self, fg_color="transparent")
        self.content.grid(row=1, column=0, sticky="nsew")

        # Make content expand
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def add_tab(self, name, frame):
        # Style your tab button here
        btn = customtkinter.CTkButton(
            self.tab_bar, 
            text=name,
            fg_color="#444",
            text_color="white",
            border_width=0,
            corner_radius=0,
            height=30,
            hover=True,
            hover_color="#666",
            command=lambda n=name: self.select_tab(n)
        )
        btn.pack(side="left", padx=(0, 2))
        self.tabs[name] = frame
        self.buttons[name] = btn

        # Ensure the tab page is not shown until selected
        try:
            frame.grid_forget()
        except Exception:
            pass

        return frame

    def select_tab(self, name):
        # Hide all frames (use grid_forget for grid-managed pages)
        for frame in self.tabs.values():
            try:
                frame.grid_forget()
            except Exception:
                try:
                    frame.pack_forget()
                except Exception:
                    pass

        # Show selected frame inside the content area
        page = self.tabs.get(name)
        if page is not None:
            page.grid(in_=self.content, row=0, column=0, sticky="nsew")

        # Update button styles
        for n, btn in self.buttons.items():
            if n == name:
                btn.configure(fg_color="#2E86C1")  # selected color
            else:
                btn.configure(fg_color="#444")     # normal color

class code():
    def color_picker():
        global color
        color = colorchooser.askcolor(title="Pick a Color")[1]
    def open_path_code():
        global file_path
        global save_path
        try:
            file_path = filedialog.askopenfilename(initialdir=os.getcwd(),filetypes=[("Word Files", "*.docx")], title="Open Word Files")
            if file_path:
                save_path = os.path.dirname(file_path)  # Set save path to the same directory as the file
            else:
                messagebox.showerror("Error", "No file selected")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")    
    
    def save_path_code():
        global save_path
        try:
            save_path = filedialog.asksaveasfilename(initialdir=os.getcwd(),filetypes=[("Word Documents", "*.docx")],title="Save as Word Document")
            if save_path:
                pass
            else:
                messagebox.showerror("Error", "No Directory selected")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def translate():
        global file_path
        global save_path
        if overwrite_value.get()==1:
            save_path = file_path
        try:
            if open_after_work.get()==1:
                translation_logic.main(question_type="mcq", file_path=file_path, save_path=save_path)
                os.startfile(save_path)  # Open the file
                
            else:
                translation_logic.main(question_type="mcq", file_path=file_path, save_path=save_path)
            messagebox.showinfo("Completed", "Translation from Bangla to English is completed.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def convert():
        global overwrite_value
        global file_path
        global save_path
        global high_value
        if overwrite_value.get()==1:
            save_path = file_path
        
        hvalue = high_value.get()
            
        
        try:
            if open_after_work.get()==1:
                convertion_logic.replace_and_highlight(file_path, save_path, hvalue)
                os.startfile(save_path)  # Open the file
            else:
                convertion_logic.replace_and_highlight(file_path, save_path, hvalue)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    


class imageframe(customtkinter.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid(row=0, column=0, sticky="nsew")
        self.create_widgets()
    
    def create_widgets(self):
        self.image1 = customtkinter.CTkImage(light_image= Image.open(img2), dark_image= Image.open(img1), size=(400,600))
        self.label1 = customtkinter.CTkLabel(self, text="", image=self.image1)
        self.label1.grid(row=0, column=0)

class convframe(customtkinter.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)        
        ##Checkbox value
        global overwrite_value
        global open_after_work
        global high_value
        high_value = customtkinter.IntVar(value=1)
        open_after_work = customtkinter.IntVar(value=1)
        overwrite_value = customtkinter.IntVar(value=1)

        self.master = master
        self.label = customtkinter.CTkLabel(self, text="Unicode to ASCII converter", font=("Arial", 20, "bold"))
        self.label.grid(row=0, column=0, padx=20, pady=20)

        self.label2 = customtkinter.CTkLabel(self, text="Open Path", font=("Arial",20,"bold"))
        self.label2.grid(row=1, column=0, padx=20, sticky="w")

        self.button1 = customtkinter.CTkButton(self, text="Browse", command= code.open_path_code, width=100, corner_radius=20, hover= True, hover_color="gray")
        self.button1.grid(row=1, column=0, pady=5, sticky="e")

        self.label3 = customtkinter.CTkLabel(self, text="Save Path", font=("Arial",20,"bold"))
        self.label3.grid(row=2, column=0, padx=20, sticky="w")

        self.button2 = customtkinter.CTkButton(self, text="Browse", command= code.save_path_code, width=100, corner_radius=20, hover= True, hover_color="gray")
        self.button2.grid(row=2, column=0, pady=5, sticky="e")  

        self.checkbox1 = customtkinter.CTkSwitch(self, text="Overwrite same file", variable=overwrite_value, font=("Arial",15,"bold"))
        self.checkbox1.grid(row=3, column=0, padx=20, pady=5, sticky="w")

        self.checkbox2 = customtkinter.CTkSwitch(self, text="Open file after convertion", variable=open_after_work, font=("Arial",15,"bold"))
        self.checkbox2.grid(row=4, column=0, padx=20, pady=5, sticky="w")

        self.checkbox3 = customtkinter.CTkSwitch(self, text="Converted text highlight", variable=high_value, font=("Arial", 15, "bold"))
        self.checkbox3.grid(row=5, column=0, padx=20, pady=5, sticky="w")

        self.conv_button = customtkinter.CTkButton(self, text="CONVERT", font=("Bahnschrift SemiBold Condensed", 30), corner_radius=20, hover= True, hover_color="green", command=code.convert)
        self.conv_button.grid(row=9, column=0, pady=20)

        #self.label4 = customtkinter.CTkLabel(self, text="Special thanks to Rashed Shan", font=("Arial", 10, "bold"))
        #self.label4.place(relx=0, rely=1.0, anchor="sw")

        #self.toggle = self.ThemeToggle(master = self, command=None)
        #self.toggle.place(relx=1.0, rely=1.0, anchor="se")

        #self.label = customtkinter.CTkLabel(self, text="Select Theme:")
        #self.label.place(relx=1.0, rely=0.95, anchor="se")
    
    def refresh_entry1(self):
        global file_path
        print (file_path)
        self.entry1.delete(0, "end")
        self.entry1.insert(0, file_path)

    class ThemeToggle(customtkinter.CTkFrame):
        def __init__(self, master, command=None, **kwargs):
            super().__init__(master, width=80, height=30, fg_color="gray", corner_radius=15, **kwargs)
            self.command = command

            # Detect the current theme and set initial state
            self.state = customtkinter.get_appearance_mode() == "Dark"

            # Sliding button
            self.button = customtkinter.CTkFrame(self, width=26, height=26, fg_color="white", corner_radius=13)
            self.button.place(x=50 if self.state else 3, y=3)  # Position based on current theme
            
            # Bind click events
            self.bind("<Button-1>", self.toggle)
            self.button.bind("<Button-1>", self.toggle)

        def toggle(self, event=None):
            self.state = not self.state  # Toggle state
            new_x = 50 if self.state else 3  # Move button
            self.animate(self.button.winfo_x(), new_x)

            # Change theme
            mode = "Dark" if self.state else "Light"
            customtkinter.set_appearance_mode(mode)

            # Call external function (if provided)
            if self.command:
                self.command(mode)

        def animate(self, start, end):
            step = 2 if start < end else -2  # Movement direction
            if abs(start - end) > 2:
                self.button.place(x=start + step, y=3)
                self.after(10, self.animate, start + step, end)  # Smooth animation
            else:
                self.button.place(x=end, y=3)
def report_issues():
    import webbrowser
    webbrowser.open("https://docs.google.com/forms/d/e/1FAIpQLSfD0Z7ZIF7GLmJNEENhhN6mvwvYRv8xapLqLLxOmXO8drRizQ/viewform?usp=sharing&ouid=112908537690851176933")


def credits():
    credit_window = customtkinter.CTk()
    credit_window.title("Version Info")
    credit_window.geometry("600x400")
    changes_label = customtkinter.CTkLabel(credit_window, text="Version: 1.0.2[1]\n\nChanges:\n- Fixed various encoding problems [thanks to Rashed Shan]\n- Minor UI adjustments", font=("Times New Roman", 20), justify="left")
    changes_label.place(relx=0, rely=0)
    report_btn = customtkinter.CTkButton(credit_window, text="Report Issues", font=("Arial", 20), hover=True, hover_color='Red', command=report_issues)
    report_btn.place(relx=0.85, rely=0.05, anchor="center")
    dev_label = customtkinter.CTkLabel(credit_window, text="{DevInfo}", font=("Courier New", 40))
    dev_label.place(relx=0.5, rely=0.35, anchor="center")
    name_label = customtkinter.CTkLabel(credit_window, text="Farias Hamid Jim", font=("Courier New", 30))
    name_label.place(relx=0, rely=0.5, anchor="w")
    mail_label = customtkinter.CTkLabel(credit_window, text="Email: fariashamid@gmail.com", font=("Courier New", 18))
    mail_label.place(relx=0, rely=0.58, anchor="w")
    pin_label = customtkinter.CTkLabel(credit_window, text="Pin- 8312", font=("Courier New", 15))
    pin_label.place(relx=0, rely=0.63, anchor="w")
    #####Fix Image loading problem
    #photo = customtkinter.CTkImage(light_image= Image.open(img3), dark_image= Image.open(img3), size=(150,150))
    #photo_label = customtkinter.CTkLabel(credit_window, text="", image=photo)  
    #photo_label.place(relx=0.75, rely=0.65, anchor="center")



    credit_window.mainloop()

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("WordBuddy")
        self.geometry("700x630")
        self.resizable(False, False)

        # Create main frame
        self.main_frame = imageframe(self)
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        # Create convframe (tabbed area)
        self.tabbed = tabbed_frame(self)
        self.tabbed.grid(row=0, column=1, sticky="nsew")

        # Add tabs - create the page with the tab's content parent
        self.tabbed.add_tab("UniToAsci", convframe(self.tabbed.content))
        self.tabbed.select_tab("UniToAsci")
        self.tabbed.add_tab("Translator", Translator(self.tabbed.content))

        #credits
        self.label = customtkinter.CTkLabel(self, text="Developed by: Farias Hamid Jim", font=("Arial", 15))
        self.label.grid(row=1, column=0, columnspan=2, pady=2, sticky="w")
        self.bt1 = customtkinter.CTkButton(self, text="Version: 1.0.2[1]", font=("Arial", 15), bg_color="white", corner_radius=0, command= lambda: credits())
        self.bt1.grid(row=1, columnspan=2, column=0, pady=0, padx=0, sticky="e")
        self.label1 = customtkinter.CTkLabel(self, text="All rights reserved", font=("Arial", 15))
        self.label1.grid(row=1, column=0, columnspan=2, pady=2, sticky="s")
        
######bypassing Init.py
app = App()
try:
    app.iconbitmap(icon)  # Set the icon for the application
except:
    pass
if __name__ == "__main__":
    app.mainloop()

