import tkinter as tk
from tkinter import messagebox
from ..database import validate_user

class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AC Workshop - Login")
        self.geometry("300x200")
        tk.Label(self, text="Username").grid(row=0, column=0, padx=10, pady=5)
        self.username = tk.Entry(self)
        self.username.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self, text="Password").grid(row=1, column=0, padx=10, pady=5)
        self.password = tk.Entry(self, show="*")
        self.password.grid(row=1, column=1, padx=10, pady=5)

        tk.Button(self, text="Login", command=self.try_login).grid(row=2, column=0, columnspan=2, pady=20)

    def try_login(self):
        if validate_user(self.username.get(), self.password.get()):
            self.destroy()
            from ..ui.main_menu import MainMenu
            MainMenu().mainloop()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")
