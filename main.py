from gui.window import MainWindow
from src.auth import gmail_authenticate
from src.email_handler import get_user_email

def main() -> None:

    # run the main frame window
    root = MainWindow()
    root.mainloop()

    # service = gmail_authenticate()
    # emails = list_emails(service)
    # store_mail_count(service, emails)
    # batch_delete(service, "email_sender_data.json")
    # print(get_user_email(service))

if __name__ == "__main__":
    main()
