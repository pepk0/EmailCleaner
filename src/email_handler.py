import tkinter
from tkinter import ttk
from gui.display_text import print_tw

from googleapiclient.errors import HttpError


def get_user_email(service) -> str:
    """ Gets the users email address
    Args:
        service (object) Gmail auth service object
    Returns:
        str: email address
    """
    user_email = "Unknown"
    try:
        user_email_address = service.users().getProfile(userId="me").execute()
        return user_email_address.get("emailAddress")
    except (HttpError, AttributeError):
        return user_email


def get_user_email_count(service) -> int:
    """ Gets the count of messages in the users mailbox
    Args:
        service (object) Gmail auth service object
    Returns:
        int: count of messages in the mailbox
    """
    count = 0
    try:
        user_email_address = service.users().getProfile(userId="me").execute()
        return user_email_address.get("messagesTotal")
    except (HttpError, AttributeError):
        return count


def get_sender(service, mail_id: str) -> str:
    """ Gets the sender of a particular email message
    Args:
        service (object) Gmail auth service object
        mail_id (str) ID string of the desired message
    Returns:
        str: the sender name and email address
    """
    sender = "Unknown"
    try:
        sender = service.users().messages().get(
            userId="me", 
            id=mail_id, 
            format="full").execute()
    except (HttpError, AttributeError):
        return sender
    for header in sender["payload"]["headers"]:
        if "From" == header["name"]:
            return header["value"]
    return sender


def list_emails(service, query=None) -> list:
    """ Gets all messages matching a query
    Args:
        service (object) Gmail auth service object
        query (str) (optional) name and email of sender
    Returns:
        list: all message id's matching the query if specified
        else of all messages
    """
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


def load_user_emails(service, list_mails: list, progress_bar: ttk.Progressbar,
                     text_progress: tkinter.Label, parent_widget: tkinter.Frame,
                     output_field: tkinter.Label) -> set:
    """ Loads all messages from the mailbox in to the app memory
    Args:
        service (object) Gmail auth service object
        progress_bar (Progressbar) reference to the progress bar widget
        text_progress (Label) reference to the text displaying widget
        parent_widget (Frame) reference to the parent widget holding 
        all the other widgets such as text and bar
        output_field (Label) reference to the widget displaying messages
    Returns:
        set: all the senders and the count of mails from them
    """
    email_senders_set = set()
    total_emails = len(list_mails)
    # gets the single mail increment value of the progress bar
    progress_increment = 100 / total_emails
    # places the bar on the app interface
    parent_widget.grid(row=2, column=0)
    for iteration, email in enumerate(list_mails, 1):
        # progress the bar
        progress_bar["value"] += progress_increment
        text_progress["text"] = f"({iteration}/{total_emails})"
        progress_bar.update()
        text_progress.update()
        email_senders_set.add(get_sender(service, email))
    # removes the progress bar after it's done
    parent_widget.grid_forget()
    print_tw(output_field, "Successfully loaded senders!", susses=True)
    return email_senders_set


def batch_delete(service, mail_id: str) -> int:
    """ PERMANENTLY deletes all emails from a particular sender
    Args:
        service (object) Gmail auth service object
        mail_id (str) the name and email of a sender
    Returns:
        int: count of all the messages deleted
    """
    deleted_messages = 0
    messages = list_emails(service, mail_id)
    while messages:
        # batch delete API cant delete more than 1k messages,
        # so we need to split them accordingly
        to_delete = messages[:1000]
        messages = messages[1000:]
        try:
            service.users().messages().batchDelete(
                userId="me", 
                body={"ids": to_delete}).execute()
            deleted_messages += len(to_delete)
        except (HttpError, AttributeError):
            continue
    return deleted_messages
