from tkinter import Frame, Label
from src.mail_service import MailService


class InfoFrame(Frame):
    def __init__(self) -> None:
        super().__init__()
        self.service = MailService()
        self.user = self.service.get_user_email()
        self.inbox = "N/A"

        self.user_label = Label(self, text=f"User: {self.user}",
                                font=("Helvetica", 14))
        self.inbox_label = Label(self, text=f"Inbox: {self.inbox}",
                                 font=("Helvetica", 14))

        # frame placement
        self.user_label.grid(row=0, column=0)
        self.inbox_label.grid(row=0, column=1, padx=60)

    def refresh_mail_count(self) -> None:
        self.inbox_label["text"] = \
            f"Inbox: {self.service.get_user_email_count()}"
