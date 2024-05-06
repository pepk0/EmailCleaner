import os.path

from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class MailService:
    SCOPES = ['https://mail.google.com/']

    def __init__(self) -> None:
        self.service = self.generate_service()

    def generate_service(self):
        creds = None
        # The file token.json stores the user's access and refresh tokens,
        # and is created automatically when the authorization flow completes
        # for the first time.
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json",
                                                          self.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except RefreshError:
                    # if the token is expired, we need to delete it and go
                    # through the youth process from the browser again
                    os.remove("token.json")
                    raise SystemExit
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", self.SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())

        try:
            # Call the Gmail API
            return build("gmail", "v1", credentials=creds)
        except HttpError:
            return False

    def get_user_email(self) -> str:
        """ Gets the users email address
        Args:
        Returns:
            str: email address
        """
        user_email = "Unknown"
        try:
            user_email_address = self.service.users().getProfile(
                userId="me").execute()
            return user_email_address.get("emailAddress")
        except (HttpError, AttributeError):
            return user_email

    def get_user_email_count(self) -> int:
        """ Gets the count of messages in the users mailbox
        Args:
        Returns:
            int: count of messages in the mailbox
        """
        count = 0
        try:
            user_email_address = self.service.users().getProfile(
                userId="me").execute()
            return user_email_address.get("messagesTotal")
        except (HttpError, AttributeError):
            return count

    def get_sender(self, mail_id: str) -> str:
        """ Gets the sender of a particular email message
        Args:
            mail_id (str) ID string of the desired message
        Returns:
            str: the sender name and email address
        """
        sender = "Unknown"
        try:
            sender = self.service.users().messages().get(
                userId="me",
                id=mail_id,
                format="full").execute()
        except (HttpError, AttributeError):
            return sender
        for header in sender["payload"]["headers"]:
            if "From" == header["name"]:
                return header["value"]
        return sender

    def list_emails(self, query=None) -> list:
        """ Gets all messages matching a query
        Args:
            query (str) (optional) name and email of sender
        Returns:
            list: all message id's matching the query if specified
            else of all messages
        """
        messages = []
        try:
            result = self.service.users().messages().list(userId="me",
                                                          q=query).execute()
        except (HttpError, AttributeError):
            return messages
        if "messages" in result:
            messages.extend(result["messages"])
        while "nextPageToken" in result:
            page_token = result["nextPageToken"]
            try:
                result = self.service.users().messages().list(
                    userId="me", q=query, pageToken=page_token).execute()
            except (HttpError, AttributeError):
                return [email["id"] for email in messages]
            if "messages" in result:
                messages.extend(result["messages"])
        return messages

    def batch_delete(self, mail_id: str) -> int:
        """ PERMANENTLY deletes all emails from a particular sender
        Args:
            mail_id (str): the name and email of a sender
        Returns:
            int: count of all the messages deleted
        """
        deleted_messages = 0
        messages = self.get_all_mail_ids(mail_id)
        while messages:
            # batch delete API cant delete more than 1k messages,
            # so we need to split them accordingly
            to_delete = messages[:1000]
            messages = messages[1000:]
            try:
                self.service.users().messages().batchDelete(
                    userId="me",
                    body={"ids": to_delete}).execute()
                deleted_messages += len(to_delete)
            except (HttpError, AttributeError):
                continue
        return deleted_messages

    def get_all_mail_ids(self, mail_id=None) -> list:
        """Returns:
            list[str]: a list with all the email id's
        """
        return [x["id"] for x in self.list_emails(mail_id)]
