from tkinter import Frame, Label
from src.mail_service import MailService


class InfoFrame(Frame):

    def __init__(self, font: str) -> None:
        super().__init__()
        self.mail_service = MailService()
        self.user: str = self.mail_service.get_user_email()
        self.user_mail_count = self.mail_service.get_user_email_count()

        # labels that represent the text in the widget
        self.user_label = Label(self, text=f"User:  {self.user}",
                                font=(font, 12))
        self.inbox = Label(self, text=f"Inbox:  {self.user_mail_count}",
                           font=(font, 12))

        # placement of the labels
        self.user_label.grid(row=0, column=0)
        self.inbox.grid(row=0, column=1, padx=50)

    def refresh(self) -> None:
        """Refreshes the mail counts in the Inbox label"""
        self.inbox["text"] = \
            f"Inbox: {self.mail_service.get_user_email_count()}"
