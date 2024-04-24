from tkinter import StringVar, Frame, ttk


class SelectionFrame(Frame):
    def __init__(self) -> None:
        super().__init__()
        self.mail_choice: StringVar = StringVar()
        self.__email_senders: set = set()
        self.__excluded_senders: set = set()

        # dropdown list for all the email senders
        self.get_mail_list = ttk.Combobox(
            self, textvariable=self.mail_choice, state="readonly",
            values=list(self.__email_senders), width=40, font=("Helvetica", 15))

        # control buttons
        self.delete_button = ttk.Button(self, text="Delete", width=10)
        self.exclude_button = ttk.Button(self, text="Exclude", width=10)
        self.clear_button = ttk.Button(self, text="Clear Excluded")

        # packing all the buttons and dropdowns in the frame
        self.get_mail_list.grid(row=0, column=0, pady=7, padx=3)
        self.delete_button.grid(row=0, column=1, padx=3)
        self.exclude_button.grid(row=0, column=2, padx=3)
        self.clear_button.grid(row=0, column=3, padx=3)

    @property
    def email_senders(self) -> set:
        return self.__email_senders

    @property
    def excluded_senders(self) -> set:
        return self.__excluded_senders

    def update_sender_list(self, new_value_list=None) -> None:
        if not new_value_list:
            new_value_list = set()
        self.__email_senders = set(new_value_list)
        self.get_mail_list["values"] = self.__email_senders

    def clear_excluded_list(self) -> None:
        self.__excluded_senders.clear()

    def clear_choice_box(self) -> None:
        self.get_mail_list.set(" ")
