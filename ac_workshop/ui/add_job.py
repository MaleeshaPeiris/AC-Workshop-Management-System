import tkinter as tk
from tkinter import messagebox
from ..models import Job
from ..database import insert_job
from datetime import datetime

class AddJobWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Add Service/Repair Info")
        self.geometry("500x700")

        self.job_type = tk.StringVar(value="Vehicle")
        self.is_service = tk.IntVar()
        self.is_repair = tk.IntVar()

        # Vehicle fields
        self.vehicle_frame = tk.Frame(self)
        tk.Label(self.vehicle_frame, text="Number Plate:").grid(row=0, column=0, sticky="w")
        self.entry_plate = tk.Entry(self.vehicle_frame)
        self.entry_plate.grid(row=0, column=1)
        tk.Label(self.vehicle_frame, text="Make:").grid(row=1, column=0, sticky="w")
        self.entry_make = tk.Entry(self.vehicle_frame)
        self.entry_make.grid(row=1, column=1)
        tk.Label(self.vehicle_frame, text="Model:").grid(row=2, column=0, sticky="w")
        self.entry_model = tk.Entry(self.vehicle_frame)
        self.entry_model.grid(row=2, column=1)
        self.vehicle_frame.grid(row=2, column=0, columnspan=2, pady=5)
        self.vehicle_frame.grid_remove()

        tk.Label(self, text="Job Type").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        tk.Radiobutton(self, text="Room", variable=self.job_type, value="Room", command=self.toggle_vehicle_fields).grid(row=1, column=1, sticky="w")
        tk.Radiobutton(self, text="Vehicle", variable=self.job_type, value="Vehicle", command=self.toggle_vehicle_fields).grid(row=0, column=1, sticky="w")
        self.toggle_vehicle_fields()

        tk.Label(self, text="Client Name").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.client_name = tk.Entry(self)
        self.client_name.grid(row=3, column=1)

        tk.Label(self, text="Phone").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.phone = tk.Entry(self)
        self.phone.grid(row=4, column=1)

        tk.Label(self, text="Job Date (YYYY-MM-DD)").grid(row=5, column=0, sticky="w", padx=5, pady=5)
        self.job_date = tk.Entry(self)
        self.job_date.insert(0, datetime.today().strftime('%Y-%m-%d'))
        self.job_date.grid(row=5, column=1)

        tk.Checkbutton(self, text="Service", variable=self.is_service, command=self.update_fields).grid(row=6, column=0, sticky="w")
        tk.Label(self, text="Service Done By").grid(row=6, column=1, sticky="w")
        self.service_by_entry = tk.Entry(self, state="disabled")
        self.service_by_entry.grid(row=7, column=1)

        tk.Checkbutton(self, text="Repair", variable=self.is_repair, command=self.update_fields).grid(row=8, column=0, sticky="w")
        tk.Label(self, text="Repair Done By").grid(row=8, column=1, sticky="w")
        self.repair_by_entry = tk.Entry(self, state="disabled")
        self.repair_by_entry.grid(row=9, column=1)

        tk.Label(self, text="Next Service Date (YYYY-MM-DD)").grid(row=10, column=0, sticky="w", padx=5, pady=5)
        self.next_service_date = tk.Entry(self)
        self.next_service_date.grid(row=10, column=1)

        tk.Label(self, text="Notes").grid(row=11, column=0, sticky="nw", padx=5, pady=5)
        self.notes = tk.Text(self, height=4, width=30)
        self.notes.grid(row=11, column=1)

        tk.Label(self, text="Total Amount").grid(row=12, column=0, sticky="w", padx=5, pady=5)
        self.total_amount = tk.Entry(self)
        self.total_amount.grid(row=12, column=1)

        button_frame = tk.Frame(self)
        button_frame.grid(row=13, column=0, columnspan=2, pady=15)
        tk.Button(button_frame, text="Save Job", command=self.save_job, width=15).pack(side="left", padx=10)
        tk.Button(button_frame, text="Back", command=self.go_back, width=15).pack(side="left", padx=10)

    def toggle_vehicle_fields(self):
        if self.job_type.get() == "Vehicle":
            self.vehicle_frame.grid()
        else:
            self.vehicle_frame.grid_remove()

    def update_fields(self):
        self.service_by_entry.config(state="normal" if self.is_service.get() else "disabled")
        if not self.is_service.get():
            self.service_by_entry.delete(0, tk.END)
        self.repair_by_entry.config(state="normal" if self.is_repair.get() else "disabled")
        if not self.is_repair.get():
            self.repair_by_entry.delete(0, tk.END)

    def save_job(self):
        if not self.client_name.get() or not self.phone.get() or not self.job_date.get():
            messagebox.showerror("Validation Error", "Client Name, Phone, and Date are required")
            return
        try:
            amount = int(self.total_amount.get() or 0)
        except ValueError:
            messagebox.showerror("Validation Error", "Total Amount must be a number")
            return
        job = Job(
            client_name=self.client_name.get(),
            phone=self.phone.get(),
            job_date=self.job_date.get(),
            is_service=self.is_service.get(),
            is_repair=self.is_repair.get(),
            service_by=self.service_by_entry.get() if self.is_service.get() else "",
            repair_by=self.repair_by_entry.get() if self.is_repair.get() else "",
            next_service_date=self.next_service_date.get(),
            notes=self.notes.get("1.0", "end").strip(),
            job_type=self.job_type.get(),
            plate=self.entry_plate.get(),
            make=self.entry_make.get(),
            model=self.entry_model.get(),
            total_amount=amount
        )
        insert_job(job)
        messagebox.showinfo("Success", "Job added successfully")
        self.go_back()

    def go_back(self):
        self.destroy()
        from ..ui.main_menu import MainMenu
        MainMenu().mainloop()
