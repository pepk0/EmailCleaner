from tkinter import Frame, Label, ttk


class LoadMailFrame(Frame):
    FONT = "Helvetica"

    def __init__(self) -> None:
        super().__init__()
        self.user: str = "popovstz@gmial.com"
        self.user_mail_count: int = 1000

        self.load_button = ttk.Button(self, text="Load Emails", width=15)
        self.status_text = Label(self, text=f"User:  {self.user}",
                                 font=(self.FONT, 12))
        self.mail_count = Label(self, text=f"Inbox:  {self.user_mail_count}",
                                font=(self.FONT, 12))

        self.status_text.grid(row=0, column=0)
        self.mail_count.grid(row=0, column=1, padx=50)
        self.load_button.grid(row=0, column=2)

