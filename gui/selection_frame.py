from tkinter import StringVar, Frame, ttk


class SelectionFrame(Frame):
    OPTION_CHOICES: list = ["Delete", "Save", "Batch Delete", "Clear Saved"]

    def __init__(self) -> None:
        super().__init__()
        self.mail_choice: StringVar = StringVar()
        self.option_choice: StringVar = StringVar()
        self.__email_senders: list = []
        self.__excluded_senders: list = []

        # dropdown list for all the email senders
        self.get_mail_list = ttk.Combobox(
            self, textvariable=self.mail_choice, state="readonly",
            values=self.__email_senders, width=40, font=("Helvetica", 15))

        self.get_option_list = ttk.Combobox(
            self, textvariable=self.option_choice, state="readonly",
            values=["Scan Inbox"], width=25, font=("Helvetica", 10))

        # control buttons
        self.execute_button = ttk.Button(self, text="Execute", width=13)

        # packing all the buttons and dropdowns in the frame
        self.get_mail_list.grid(row=0, column=0, pady=7, padx=3)
        self.get_option_list.grid(row=0, column=1, padx=3)
        self.execute_button.grid(row=0, column=2, padx=3)

        self.get_option_list.set("Scan Inbox")

    def set_choices(self) -> None:
        self.get_mail_list["values"] = self.__email_senders

    def update_choices(self, new_senders: set) -> None:
        self.__email_senders = [x for x in new_senders]
        self.set_choices()

    def remove_from_mail_list(self, mail: str) -> None:
        self.__email_senders.remove(mail)
        self.set_choices()

    def add_to_mail_list(self, mail: str) -> None:
        self.__email_senders.append(mail)
        self.set_choices()

    def clear_excluded_list(self) -> None:
        self.__excluded_senders.clear()

    def add_to_excluded_list(self, mail: str) -> None:
        self.__excluded_senders.append(mail)

    @property
    def excluded_senders(self) -> list:
        return self.__excluded_senders

    def load_option_choices(self) -> None:
        self.get_option_list.set(" ")
        self.get_option_list["values"] = self.OPTION_CHOICES

    def get_mail_choice(self) -> str:
        mail_choice = self.mail_choice.get()
        self.mail_choice.set(" ")
        return mail_choice

    def get_option(self) -> str:
        return self.option_choice.get()
