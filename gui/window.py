import tkinter as tk
from tkinter import ttk

from src.auth import gmail_authenticate
from src.email_handler import *


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
        self.font = "Helvetica"

        def add_to_delete() -> None:
            chosen_email = mail_choice.get()
            to_delete.append(chosen_email)
            choices.remove(chosen_email)
            get_mail['values'] = list(choices)
            get_mail.set(f"Success! Pending Deletion {len(to_delete)}")
            print(to_delete)

        def clear_choice() -> None:
            for mail in to_delete:
                choices.add(mail)
            to_delete.clear()
            get_mail['values'] = list(choices)
            get_mail.set(f"List cleared! Pending Deletion {len(to_delete)}")
            print(to_delete)

        def read_delete() -> None:
            if to_delete:
                for email_id in to_delete:
                    batch_delete(self.service, email_id)
            else:
                chosen_email = mail_choice.get()
                batch_delete(self.service, chosen_email)
                choices.remove(chosen_email)
            total_mail_count["text"] = (
                f"Total mail: {get_user_email_count(self.service)}")
            get_mail['values'] = list(choices)
            get_mail.set("Success!")

        # connection status message label and user display field
        status = tk.LabelFrame(self, text="Status:",
                               borderwidth=4, font=(self.font, 15))
        total_mail_count = tk.Label(
            status,  text=f"Total mail: {self.mail_count}")
        status_text = tk.Label(
            status, text=f"Connected as: {self.user}", font=(self.font, 12))
        if not self.service:
            status_text = tk.Label(
                status, text="Offline", font=(self.font, 12))

        # deletion and read mail section:
        to_delete = []
        choices = set([get_sender(id, self.service) for id in self.list_mails])
        mail_choice = tk.StringVar()

        delete_and_read_frame = tk.LabelFrame(
            self, text="Delete or Read", font=(self.font, 15))
        get_mail = ttk.Combobox(
            delete_and_read_frame, textvariable=mail_choice, state="readonly",
            values=list(choices), width=42, font=(self.font, 14))
        delete_button = ttk.Button(
            delete_and_read_frame, text="Delete", width=15, command=read_delete)
        add_button = ttk.Button(delete_and_read_frame,
                                text="Add", width=15, command=add_to_delete)
        clear_button = ttk.Button(delete_and_read_frame, text="Clear Added",
                                  width=15, command=clear_choice)

        # placement of widgets
        # status and info
        status.grid(row=0, column=0)
        status_text.grid(row=0, column=0,)
        total_mail_count.grid(row=1, column=0, columnspan=2)

        # mail manipulation
        delete_and_read_frame.grid(row=1, column=0)
        get_mail.grid(row=0, column=0, columnspan=3)
        delete_button.grid(row=1, column=0)
        add_button.grid(row=1, column=1)
        clear_button.grid(row=1, column=2)
