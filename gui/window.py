import tkinter as tk
from tkinter import ttk

from src.auth import gmail_authenticate
from src.email_handler import get_sender, get_user_email, list_emails


class MainWindow(tk.Tk):
    def __init__(self,) -> None:
        super().__init__()
        self.title("Pidgin")
        self.geometry("800x300")
        self.resizable(False, False)
        self.service = gmail_authenticate()
        self.connection_status = bool(self.service)
        self.user = get_user_email(self.service)
        self.list_mails = list_emails(self.service)
        self.mail_count = len(self.list_mails)

        # connection status message label and user display field
        status = tk.LabelFrame(self, text="Status:",
                               borderwidth=4, font=("Helvetica", 15))
        status_text = tk.Label(
            status, text=f"Connected as {self.user}", font=("Helvetica", 12))
        if not self.service:
            status_text = tk.Label(
                status, text="Offline", font=("Helvetica", 12))

        # deletion and read mail section:
        delete_and_read_frame = tk.LabelFrame(
            self, text="Delete or Read", font=("Helvetica", 15))
        mail_choice = tk.StringVar()
        choices = set([get_sender(id, self.service) for id in self.list_mails])
        get_mail = ttk.Combobox(
            delete_and_read_frame, textvariable=mail_choice,
            values=list(choices), width=34)
        delete_button = ttk.Button(
            delete_and_read_frame, text="Delete", width=17)
        read_button = ttk.Button(delete_and_read_frame, text="Read", width=17)

        # placement of widgets
        status.grid(row=0, column=0)
        status_text.grid(row=0, column=0, pady=10)
        delete_and_read_frame.grid(row=1, column=0)
        get_mail.grid(row=0, column=0, columnspan=2)
        delete_button.grid(row=1, column=0)
        read_button.grid(row=1, column=1)
