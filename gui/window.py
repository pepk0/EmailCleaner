import tkinter as tk
from tkinter import ttk
from gui.display_text import print_tw

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
            get_mail.set(" ")
            if chosen_email in choices:
                excluded.append(chosen_email)
                choices.remove(chosen_email)
                get_mail['values'] = list(choices)
                print_tw(message_filed, f"Emails from: {chosen_email} "
                         f"are now excluded\nExcluded senders: {len(excluded)}")
            else:
                print_tw(message_filed, "None selected!", error=True)

        def clear_choice() -> None:
            for mail in excluded:
                choices.add(mail)
            excluded.clear()
            get_mail['values'] = list(choices)
            print_tw(message_filed, f"Excluded list cleared!", susses=True)

        def delete() -> None:
            deleted_mail = 0
            if excluded:
                for email_id in choices:
                    if email_id not in excluded:
                        deleted_mail += batch_delete(self.service, email_id)
                # remove the deleted mail and replace it with the excluded
                choices.clear()
                for mail in excluded:
                    choices.add(mail)
                excluded.clear()
            else:
                get_mail.set(" ")
                chosen_email = mail_choice.get()
                if chosen_email not in choices:
                    print_tw(message_filed, "None selected!", error=True)
                    return
                deleted_mail = batch_delete(self.service, chosen_email)
                choices.remove(chosen_email)
            mail_count["text"] = f"Emails: {get_user_email_count(self.service)}"
            # add the choices to the widget
            get_mail['values'] = list(choices)
            print_tw(message_filed,
                     f"{deleted_mail} emails successfully removed", susses=True)

        # connection status message and mail count field
        status = tk.Label()
        status_text = tk.Label(
            status, text=f"Connected as: {self.user}", font=(self.font, 12))
        mail_count = tk.Label(
            status, text=f"Emails: {self.mail_count}", font=(self.font, 12))
        if not self.service:
            status_text = tk.Label(
                status, text="Offline", font=(self.font, 12))

        # deletion and read mail section filed
        excluded = []
        choices = set([get_sender(self.service, id) for id in self.list_mails])
        mail_choice = tk.StringVar()
        delete_frame = tk.Label(self, text="Delete Emails", font=(
            self.font, 15), borderwidth=5, border=5)
        get_mail = ttk.Combobox(
            delete_frame, textvariable=mail_choice, state="readonly",
            values=list(choices), width=40, font=(self.font, 14))
        delete_button = ttk.Button(
            delete_frame, text="Delete", width=10, command=delete)
        exclude_button = ttk.Button(delete_frame,
                                    text="Exclude", width=10, command=add_excluded)
        clear_button = ttk.Button(delete_frame, text="Clear Excluded",
                                  width=10, command=clear_choice)

        # text filed for message displaying
        message_filed = tk.Text(self, font=(self.font, 18), width=61)

        # status and info placement
        status.grid(row=0, column=0)
        # inside status frame placement
        status_text.grid(row=0, column=0)
        mail_count.grid(row=0, column=1, padx=50)

        # delete frame placement
        delete_frame.grid(row=1, column=0, pady=20)
        # inside delete frame placement
        get_mail.grid(row=0, column=0,  pady=7)
        delete_button.grid(row=0, column=1)
        exclude_button.grid(row=0, column=2, padx=5)
        clear_button.grid(row=0, column=3)

        # text filed and message placement
        message_filed.grid(row=2, column=0, columnspan=10)
