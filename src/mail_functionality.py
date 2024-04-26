from src.mail_service import MailService
from gui.selection_frame import SelectionFrame
from gui.message_dispaly import MessageDisplay


class MailFunctionality:
    def __init__(self) -> None:
        self.mail_service = MailService()
        self.__function_mapping = {"Scan Inbox": self.__scan_emails}

    def __scan_emails(self, selection: SelectionFrame,
                      display: MessageDisplay) -> None:
        total_emails = self.mail_service.get_all_mail_ids()
        len_emails = len(total_emails)
        mail_senders = set()
        for number, mail in enumerate(total_emails, 1):
            mail_sender = self.mail_service.get_sender(mail)
            mail_senders.add(mail_sender)
            count = display.progres_tracker(number, len_emails)
            display.display_text(f"Scanning Inbox ... {count}")
        selection.update_choices(mail_senders)
        selection.load_option_choices()
        display.display_text("Scanning Inbox Finished!", "green")

    def get_func(self, function: str):
        return self.__function_mapping.get(function, False)
