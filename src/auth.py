import os
import pickle

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError


# Request all access 
SCOPES = ['https://mail.google.com/']
PERSONAL_EMAIL = 'popovstz@gmail.com'


def gmail_authenticate() -> object:
    """ Authenticates the user, so he can use the Gmail API
    Args:
        None
    Returns:
        GoogleClient object: object which calls the Gmail API service 
    """
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    
    # if there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    try:
        return build('gmail', 'v1', credentials=creds)
    except HttpError:
        return False
