import tkinter as tk

class MainMenu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AC Workshop - Main Menu")
        self.geometry("300x250")

        tk.Label(self, text="Welcome to AC Workshop", font=("Helvetica", 14)).pack(pady=20)
        tk.Button(self, text="Add Service/Repair", width=25, command=self.open_add_job).pack(pady=10)
        tk.Button(self, text="Upcoming Services", width=25, command=self.open_upcoming).pack(pady=10)

    def open_add_job(self):
        self.destroy()
        from ..ui.add_job import AddJobWindow
        AddJobWindow().mainloop()

    def open_upcoming(self):
        self.destroy()
        from ..ui.upcoming import UpcomingServicesWindow
        UpcomingServicesWindow().mainloop()
