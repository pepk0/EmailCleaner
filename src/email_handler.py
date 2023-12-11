import tkinter as tk
from googleapiclient.errors import HttpError

from gui.display_text import print_pbar, print_tw


def get_user_email(service) -> str:
    try:
        user_email_address = service.users().getProfile(userId="me").execute()
        return user_email_address.get("emailAddress")
    except (HttpError, AttributeError):
        return "Unknown"


def get_user_email_count(service) -> int:
    count = 0
    try:
        user_email_address = service.users().getProfile(userId="me").execute()
        return user_email_address.get("messagesTotal")
    except (HttpError, AttributeError):
        return count


def get_sender(service, mai_id: str):
    try:
        sender = service.users().messages().get(
            userId="me", id=mai_id, format="full").execute()
    except (HttpError, AttributeError):
        return "Unknown"
    payload = sender.get("payload")
    headers = payload.get("headers")
    for header in headers:
        if header["name"] == "From":
            return header["value"]
    else:
        return "Unknown"


def list_emails(service, query=None) -> list:
    messages = []
    try:
        result = service.users().messages().list(userId="me", q=query).execute()
    except (HttpError, AttributeError):
        return messages
    if "messages" in result:
        messages.extend(result["messages"])
    while "nextPageToken" in result:
        page_token = result["nextPageToken"]
        try:
            result = service.users().messages().list(
                userId="me", q=query, pageToken=page_token).execute()
        except (HttpError, AttributeError):
            return [email["id"] for email in messages]
        if "messages" in result:
            messages.extend(result["messages"])
    return [email["id"] for email in messages]


def store_mail_count(service, list_mails: list, widget: tk.Text) -> dict:
    mails_as_dict = {}
    total_emails = len(list_mails)
    for iteration, email in enumerate(list_mails, 1):
        progress_bar = print_pbar(iteration, total_emails)
        print_tw(widget, f"{progress_bar}")
        widget.update()
        email_sender = get_sender(service, email)
        if email_sender not in mails_as_dict:
            mails_as_dict[email_sender] = 0
        mails_as_dict[email_sender] += 1
    else:
        print_tw(widget, "", susses=True, clear=False)
    return mails_as_dict

    

def batch_delete(service, mail_id: str) -> int:
    deleted_messages = 0
    messages = list_emails(service, mail_id)
    while messages:
        to_delete = messages[:1000]
        messages = messages[1000:]
        try:
            service.users().messages().batchDelete(
                userId="me", body={"ids": to_delete}).execute()
            deleted_messages += len(to_delete)
        except (HttpError, AttributeError):
            continue
    return deleted_messages