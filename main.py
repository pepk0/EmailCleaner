from src.set_connect import gmail_authenticate
from src.email_handler import list_emails, store_mail_count, get_name_of_sender, batch_delete


def main():

    # connection to Gmail API service
    service = gmail_authenticate()

    emails = list_emails(service)
    store_mail_count(service, emails)
    # batch_delete(service, "email_sender_data.json")

if __name__ == "__main__":
    main()
