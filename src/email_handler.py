import json
from googleapiclient.errors import HttpError


def get_user_email(service) -> str:
    try:
        user_email_address = service.users().getProfile(userId="me").execute()
        return user_email_address.get("emailAddress")
    except (HttpError, AttributeError):
        return "Unknown"


def get_user_email_count(service) -> str:
    try:
        user_email_address = service.users().getProfile(userId="me").execute()
        return user_email_address.get("messagesTotal")
    except (HttpError, AttributeError):
        return "0"


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


def store_mail_count(service, messages: list) -> list:
    mails_as_dict = {}
    for email_id in messages:
        sender = get_sender(email_id, service)
        if sender not in mails_as_dict:
            mails_as_dict[sender] = 0
        mails_as_dict[sender] += 1
    # save data as a json
    with open("email_sender_data.json", "w", encoding="utf-8") as json_file:
        json.dump(mails_as_dict, json_file, indent=4)
    return [mail_name for mail_name in mails_as_dict.keys()]


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