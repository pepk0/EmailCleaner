import json
from googleapiclient.errors import HttpError


def get_user_email(service) -> str:
    try:
        user_email_address = service.users().getProfile(userId="me").execute()
        return user_email_address.get("emailAddress")
    except HttpError and AttributeError:
        return "Unknown"


def get_name_of_sender(mai_id: str, service):
    try:
        sender = service.users().messages().get(
            userId="me", id=mai_id, format="full").execute()
    except HttpError or AttributeError:
        return "Unknown"
    payload = sender.get("payload")
    headers = payload.get("headers")
    for header in headers:
        if header["name"] == "From":
            return header["value"]


def list_emails(service, query=None) -> list:
    messages = []
    try:
        result = service.users().messages().list(userId="me", q=query).execute()
    except HttpError or AttributeError:
        return [email["id"] for email in messages]
    if "messages" in result:
        messages.extend(result["messages"])
    while "nextPageToken" in result:
        page_token = result["nextPageToken"]
        try:
            result = service.users().messages().list(
                userId="me", q=query, pageToken=page_token).execute()
        except HttpError:
            return [email["id"] for email in messages]
        if "messages" in result:
            messages.extend(result["messages"])

    return [email["id"] for email in messages]


def store_mail_count(service, messages: list) -> None:
    mails_as_dict = {}
    for email_id in messages:
        sender = get_name_of_sender(email_id, service)
        if sender not in mails_as_dict:
            mails_as_dict[sender] = 0
        mails_as_dict[sender] += 1
    # save data as a json
    with open("email_sender_data.json", "w", encoding="utf-8") as json_file:
        json.dump(mails_as_dict, json_file, indent=4)


def batch_delete(service, json_file_path: str) -> None:
    try:
        with open(json_file_path, "r") as email_json:
            messages = [mail_id for mail_id in json.load(email_json).keys()]
    except FileNotFoundError:
        print("missing json file")
        return
    while messages:
        mail_id = messages.pop()
        all_messages_from_user = list_emails(service, query=mail_id)
        if all_messages_from_user:
            if len(all_messages_from_user) > 1000:
                # Gmail API doesn't allow more then 1k deletes so we requeue it
                all_messages_from_user = all_messages_from_user[:1000]
                messages.append(mail_id)
            try:
                service.users().messages().batchDelete(
                    userId="me", body={"ids": all_messages_from_user}).execute()
            except HttpError:
                continue
