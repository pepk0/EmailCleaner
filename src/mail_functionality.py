from src.mail_service import MailService
from gui.selection_frame import SelectionFrame
from gui.message_dispaly import MessageDisplay


class MailFunctionality:
    def __init__(self) -> None:
        self.mail_service = MailService()
            "Scan Inbox": self.__scan_emails,
            "Delete": self.__delete_single_mail,
            "Save": self.__save_email,
            "Clear Saved": self.__clear_saved_emails
        }

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

    def __delete_single_mail(self, selection: SelectionFrame,
                             display: MessageDisplay) -> None:
        mail_to_delete = selection.get_mail_choice()
        display.display_text(f"Deleting Emails ... from {mail_to_delete}")
        deleted_mail = self.mail_service.batch_delete(mail_to_delete)
        if deleted_mail:
            selection.remove_from_mail_list(mail_to_delete)
            message = f"Successfully Deleted {deleted_mail} Emails"
            color = "green"
        else:
            message, color = "Something went wrong!", "red"
        display.display_text(message, color)

    @staticmethod
    def __save_email(selection: SelectionFrame,
                     display: MessageDisplay) -> None:
        mail_to_save = selection.get_mail_choice()
        selection.add_to_excluded_list(mail_to_save)
        selection.remove_from_mail_list(mail_to_save)
        display.display_text(
            f"Emails from {mail_to_save} are will be saved from deletion")

    @staticmethod
    def __clear_saved_emails(selection: SelectionFrame,
                             display: MessageDisplay) -> None:
        excluded_emails = selection.excluded_senders
        for mail in excluded_emails:
            selection.add_to_mail_list(mail)
        selection.clear_excluded_list()
        display.display_text("Saved Emails Cleared!", "green")

    def get_func(self, function: str):
        return self.__function_mapping.get(function, False)
