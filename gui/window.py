import tkinter as tk
from gui.selection_frame import SelectionFrame
from gui.message_display import MessageDisplay
from gui.info_frame import InfoFrame
from src.mail_functionality import MailFunctionality
from settings.settings import FONT


class MainWindow(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Email Cleaner")
        self.geometry("800x260")
        self.resizable(False, False)

        # this class holds and a mapping of the functions
        # that correspond to the options
        self.mail_functionality = MailFunctionality()

        # all the frames making up the app interface
        self.selection_frame = SelectionFrame(FONT)
        self.message_frame = MessageDisplay(FONT)
        self.info_frame = InfoFrame(FONT)

        # adds the execute function to the button on the selection frame
        self.selection_frame.execute_button["command"] = self.execute

        # frame placement
        self.info_frame.grid(row=0, column=0)
        self.selection_frame.grid(row=1, column=0, pady=20)
        self.message_frame.grid(row=2, column=0)

    def execute(self) -> None:
        """Executes the chosen option from the user"""
        mail_altering_functions = {"Delete", "Batch Delete"}
        wanted_function = self.selection_frame.get_option()
        if wanted_function:
            func = self.mail_functionality.get_func(wanted_function)
            func(self.selection_frame, self.message_frame)
            if wanted_function in mail_altering_functions:
                self.info_frame.refresh()
            return
        self.message_frame.display_text("Invalid option!", "red")
