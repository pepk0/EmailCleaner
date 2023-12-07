import tkinter as tk
from tkinter import ttk

from src.auth import gmail_authenticate
from src.email_handler import get_user_email


class MainWindow(tk.Tk):
    def __init__(self,) -> None:
        super().__init__()
        self.title("Pidgin")
        self.geometry("800x300")
        self.resizable(False, False)
        self.service = gmail_authenticate()
        self.user = get_user_email(self.service)
        self.connection_status = bool(self.service)

        # connection status message label and user display field
        status_label = tk.Label(text="Status:", font=("Helvetica", 18))
        status = tk.Label(text="Offline", fg="Red", font=("Helvetica", 18))
        user_welcome = tk.Label(
            text=f"User: {self.user}", font=("Helvetica", 18))
        if self.connection_status:
            status = tk.Label(text="Connected", fg="Green",
                            font=("Helvetica", 18))
            user_welcome = tk.Label(text=f"User: {self.user}",
                                    font=("Helvetica", 18))

        # placement of all the widgets
        user_welcome.grid(row=0, column=0, padx=30)
        status_label.grid(row=0, column=1)
        status.grid(row=0, column=2)
