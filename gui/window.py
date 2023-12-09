import tkinter as tk
from tkinter import ttk

from src.auth import gmail_authenticate
from src.email_handler import *


class MainWindow(tk.Tk):
    def __init__(self,) -> None:
        super().__init__()
        self.title("Pidgin")
        self.geometry("800x300")
        self.font = "Helvetica"
        self.resizable(False, False)
        self.service = gmail_authenticate()
        self.connection_status = bool(self.service)
        self.user = get_user_email(self.service)
        self.list_mails = list_emails(self.service)
        self.mail_count = len(self.list_mails)

        def add_excluded() -> None:
            chosen_email = mail_choice.get()
            get_mail.set("None selected!")
            if chosen_email in choices:
                excluded.append(chosen_email)
                choices.remove(chosen_email)
                get_mail['values'] = list(choices)
                get_mail.set(f"Success! Excluded mails {len(excluded)}")
                print(excluded)

        def clear_choice() -> None:
            for mail in excluded:
                choices.add(mail)
            excluded.clear()
            get_mail['values'] = list(choices)
            get_mail.set(f"List cleared! Excluded {len(excluded)}")
            print(excluded)

        def delete() -> None:
            if excluded:
                for email_id in self.list_mails:
                    if email_id not in excluded:
                        batch_delete(self.service, email_id)
            else:
                chosen_email = mail_choice.get()
                if chosen_email not in choices:
                    get_mail.set("None selected!")
                    return
                batch_delete(self.service, chosen_email)
                choices.remove(chosen_email)
            total_mail_count["text"] = (
                f"Emails: {get_user_email_count(self.service)}")
            get_mail['values'] = list(choices)
            get_mail.set("Success!")

        # connection status message and mail count field
        status = tk.LabelFrame(self, text="Status:",
                               borderwidth=4, font=(self.font, 15))
        total_mail_count = tk.Label(status, text=f"Emails: {self.mail_count}")
        status_text = tk.Label(
            status, text=f"Connected as: {self.user}", font=(self.font, 12))
        if not self.service:
            status_text = tk.Label(
                status, text="Offline", font=(self.font, 12))

        # deletion and read mail section filed
        excluded = []
        choices = set([get_sender(id, self.service) for id in self.list_mails])
        mail_choice = tk.StringVar()
        delete_and_read_frame = tk.LabelFrame(
            self, text="Delete or Read", font=(self.font, 15), borderwidth=5, border=5)
        get_mail = ttk.Combobox(
            delete_and_read_frame, textvariable=mail_choice, state="readonly",
            values=list(choices), width=42, font=(self.font, 14))
        delete_button = ttk.Button(
            delete_and_read_frame, text="Delete", width=15, command=delete)
        exclude_button = ttk.Button(delete_and_read_frame,
                                    text="Exclude", width=15, command=add_excluded)
        clear_button = ttk.Button(delete_and_read_frame, text="Clear Excluded",
                                  width=15, command=clear_choice)

        # status and info placement
        status.grid(row=0, column=0)
        # inside status frame placement
        status_text.grid(row=0, column=0,)
        total_mail_count.grid(row=1, column=0)

        # delete frame placement
        delete_and_read_frame.grid(row=1, column=0, pady=10)
        # inside delete frame placement
        get_mail.grid(row=0, column=0, columnspan=3)
        delete_button.grid(row=1, column=0)
        exclude_button.grid(row=1, column=1)
        clear_button.grid(row=1, column=2)
