from tkinter import Frame, Label
from src.mail_service import MailService


class LoadMailFrame(Frame):
    FONT = "Helvetica"

    def __init__(self) -> None:
        super().__init__()
        self.mail_service = MailService()
        self.user: str = self.mail_service.get_user_email()
        self.user_mail_count = "N/A"

        self.user_label = Label(self, text=f"User:  {self.user}",
                                font=(self.FONT, 12))
        self.inbox = Label(self, text=f"Inbox:  {self.user_mail_count}",
                           font=(self.FONT, 12))

        self.user_label.grid(row=0, column=0)
        self.inbox.grid(row=0, column=1, padx=50)

    def refresh(self) -> None:
        self.inbox["text"] = \
            f"Inbox: {self.mail_service.get_user_email_count()}"
