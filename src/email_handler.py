import json


def get_name_of_sender(mai_id: str, service):
    sender = service.users().messages().get(
        userId="me", id=mai_id, format="full").execute()
    payload = sender.get("payload")
    headers = payload.get("headers")
    for header in headers:
        if header["name"] == "From":
            return header["value"]


def list_emails(service, query=None) -> list:
    messages = []
    result = service.users().messages().list(userId="me", q=query).execute()

    if "messages" in result:
        messages.extend(result["messages"])

    while "nextPageToken" in result:
        page_token = result["nextPageToken"]
        result = service.users().messages().list(
            userId="me", q=query, pageToken=page_token).execute()
        if "messages" in result:
            messages.extend(result["messages"])

    return [email["id"] for email in messages]


def store_mail_count(service, messages: list) -> None:
    total_email_messages = len(messages)
    mails_as_dict = {}
    for email_number, email_id in enumerate(messages, 1):
        sender = get_name_of_sender(email_id, service)

        # simple CLI text to track progress
        print(f"{email_number}/{total_email_messages} -- {sender}")

        if sender not in mails_as_dict:
            mails_as_dict[sender] = 0
        mails_as_dict[sender] += 1

    # save data as a json
    with open("email_sender_data.json", "w", encoding="utf-8") as json_file:
        json.dump(mails_as_dict, json_file, indent=4)


def batch_delete(service, json_file_path: str) -> None:
    try:
        with open(json_file_path, "r") as email_json:
            all_messages = [mail_id for mail_id in json.load(email_json).keys()]
    except FileNotFoundError:
        print("missing json file")
        return
    
    while all_messages:
        mail_id = all_messages.pop()
        all_messages_from_user = list_emails(service, query=mail_id)
        if all_messages_from_user:
            if len(all_messages_from_user) > 1000:
                all_messages_from_user = all_messages_from_user[:1000]
                all_messages.append(mail_id)
            service.users().messages().batchDelete(
                userId="me", body={"ids": all_messages_from_user}).execute()
