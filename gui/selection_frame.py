from tkinter import StringVar, Frame, ttk


class SelectionFrame(Frame):
    OPTION_CHOICES: list = ["Delete", "Save", "Batch Delete", "Clear Saved"]

    def __init__(self, font: str) -> None:
        super().__init__()
        self.mail_choice: StringVar = StringVar()
        self.option_choice: StringVar = StringVar()
        self.__email_senders: list = []
        self.__excluded_senders: list = []

        # dropdown list for all the email senders
        self.get_mail_list = ttk.Combobox(
            self, textvariable=self.mail_choice, state="readonly",
            values=self.__email_senders, width=40, font=(font, 15))

        # dropdown for the options
        self.get_option_list = ttk.Combobox(
            self, textvariable=self.option_choice, state="readonly",
            values=["Scan Inbox"], width=25, font=(font, 10))

        # control button
        self.execute_button = ttk.Button(self, text="Execute", width=13)

        # dropdown menus and button placement
        self.get_mail_list.grid(row=0, column=0, pady=7, padx=3)
        self.get_option_list.grid(row=0, column=1, padx=3)
        self.execute_button.grid(row=0, column=2, padx=3)

        # sets the initial value to Scan Inbox witch is the only option,
        # since we need to have emails to conduct operations on them
        self.get_option_list.set("Scan Inbox")

    @property
    def excluded_senders(self) -> list:
        return self.__excluded_senders

    @property
    def email_senders(self) -> list:
        return self.__email_senders

    def set_choices(self) -> None:
        """Sets the email drop down values equal to the email senders values."""
        self.get_mail_list["values"] = self.__email_senders

    def update_choices(self, new_senders=None, clear=False) -> None:
        """sets the given iterable in the mail selection dropdown menu.
        Args:
            new_senders:
            (iterable) this will be set as the mail choices in
            the dropdown menu.
            clear: (bool) this controls if the menu is set as an empty list,
            thus clearing the email choices.
        """
        if clear and not new_senders:
            new_senders = []
        self.__email_senders = [x for x in new_senders]
        self.set_choices()

    def remove_from_mail_list(self, mail: str) -> None:
        """Removes the item from the mail senders list.
        Args:
            mail: (str) the mail that will be removed.
        """
        self.__email_senders.remove(mail)
        self.set_choices()

    def add_to_mail_list(self, mail: str) -> None:
        """Adds an item to the mail senders list.
        Args:
            mail: (str) the mail that will be added.
        """
        self.__email_senders.append(mail)
        self.set_choices()

    def clear_excluded_list(self) -> None:
        """Clears the excluded list."""
        self.__excluded_senders.clear()

    def add_to_excluded_list(self, mail: str) -> None:
        """Adds an item to the saved senders list.
        Args:
            mail: (str): the mail that will be added.
        """
        self.__excluded_senders.append(mail)

    def load_option_choices(self) -> None:
        """Loads the options in to the option drop down menu."""
        self.get_option_list.set("")
        self.get_option_list["values"] = self.OPTION_CHOICES

    def get_mail_choice(self) -> str:
        """Retrieves the mail selected from the user.
        Returns:
            (str) the mail selected from the user and sets the mail
            dropdown as blank.
        """
        mail_choice = self.mail_choice.get()
        self.mail_choice.set("")
        return mail_choice

    def get_option(self) -> str | None:
        """Gets the option selected from the user.
        Returns:
            (str) the option selected from the option dropdown menu.
        """
        option = self.option_choice.get()
        if option == "Scan Inbox":
            self.get_option_list.set("")
        return option if option else None
