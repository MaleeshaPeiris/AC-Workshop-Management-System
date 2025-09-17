import tkinter as tk
from tkinter import ttk
from ac_workshop.database import get_upcoming_services

class UpcomingServicesWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Upcoming Services")
        self.geometry("750x400")

        self.filter_type = tk.StringVar(value="All")
        self.period = tk.StringVar(value="Week")

        tk.Label(self, text="Filter by Type", font=("Helvetica", 12)).pack(pady=5)
        filter_frame = tk.Frame(self)
        filter_frame.pack()
        tk.Radiobutton(filter_frame, text="All", variable=self.filter_type, value="All", command=self.load_data).grid(row=0, column=0, padx=5)
        tk.Radiobutton(filter_frame, text="Rooms", variable=self.filter_type, value="Room", command=self.load_data).grid(row=0, column=1, padx=5)
        tk.Radiobutton(filter_frame, text="Vehicles", variable=self.filter_type, value="Vehicle", command=self.load_data).grid(row=0, column=2, padx=5)

        tk.Label(self, text="Show services within:", font=("Helvetica", 12)).pack(pady=5)
        period_combo = ttk.Combobox(self, textvariable=self.period, values=["Week", "Month", "Three Months", "Year"], state="readonly", width=10)
        period_combo.pack()
        period_combo.bind("<<ComboboxSelected>>", lambda e: self.load_data())

        columns = ("name", "phone", "job_type", "next_service", "plate", "make", "model")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col.capitalize())
        self.tree.pack(fill="both", expand=True, pady=10)

        tk.Button(self, text="Back", command=self.go_back).pack(pady=10)

        self.load_data()

    def load_data(self):
        self.tree.delete(*self.tree.get_children())
        rows = get_upcoming_services(self.filter_type.get(), days=self.period.get())
        for row in rows:
            self.tree.insert("", "end", values=row)

    def go_back(self):
        self.destroy()
        from ac_workshop.ui.main_menu import MainMenu
        MainMenu().mainloop()
