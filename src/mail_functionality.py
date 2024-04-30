from src.mail_service import MailService
from gui.selection_frame import SelectionFrame
from gui.message_dispaly import MessageDisplay


class MailFunctionality:
    def __init__(self) -> None:
        self.mail_service = MailService()
        self.__function_mapping = {
            "Scan Inbox": self.__scan_emails,
            "Delete": self.__delete_single_mail,
            "Save": self.__save_email,
            "Batch Delete": self.__batch_delete,
            "Clear Saved": self.__clear_saved_emails,
        }

    def __scan_emails(self, selection: SelectionFrame,
                      display: MessageDisplay) -> None:
        """Scans the email inbox, and gathers info about the emails"""
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
        """Deletes a single mail that is selected"""
        mail_to_delete = selection.get_mail_choice()
        if not mail_to_delete:
            display.display_text("No mails selected!", "red")
            return
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
        """Saves a mail from deletion"""
        mail_to_save = selection.get_mail_choice()
        if not mail_to_save:
            display.display_text("No mails selected!", "red")
            return
        selection.add_to_excluded_list(mail_to_save)
        selection.remove_from_mail_list(mail_to_save)
        display.display_text(
            f"Emails from: {mail_to_save}, will be saved from deletion")

    @staticmethod
    def __clear_saved_emails(selection: SelectionFrame,
                             display: MessageDisplay) -> None:
        """Removes all mail previously saved, making it deletable"""
        excluded_emails = selection.excluded_senders
        if not excluded_emails:
            display.display_text("No saved emails currently!", "red")
            return
        for mail in excluded_emails:
            selection.add_to_mail_list(mail)
        selection.clear_excluded_list()
        display.display_text("Saved emails are now cleared!", "green")

    def __batch_delete(self, selection: SelectionFrame,
                       display: MessageDisplay) -> None:
        """Deletes all the mail except the mail in that is saved"""
        deleted_mail = 0
        for mail in selection.email_senders:
            if mail not in selection.excluded_senders:
                display.display_text(f"Deleting mail from {mail}")
                deleted_mail += self.mail_service.batch_delete(mail)
        selection.update_choices(clear=True)
        display.display_text(
            f"Deleted a total of {deleted_mail} emails!", "green")

    def get_func(self, function: str):
        """Returns a function based on the option selected"""
        return self.__function_mapping.get(function, False)
