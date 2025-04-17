import customtkinter as ctk

app = ctk.CTk()
app.geometry("400x300")

# Create the tabview
tabview = ctk.CTkTabview(master=app)
tabview.pack(padx=20, pady=20, fill="both", expand=True)

# Add tabs (this is correct)
tabview.add("Tab 1")
tabview.add("Tab 2")
tabview.add("Settings")

# Add widgets to a specific tab
ctk.CTkLabel(tabview.tab("Tab 1"), text="Hello from Tab 1").pack(pady=10)
ctk.CTkButton(tabview.tab("Tab 1"), text="Hello").pack()
ctk.CTkLabel(tabview.tab("Tab 2"), text="Tab 2 content here").pack(pady=10)

app.mainloop()
