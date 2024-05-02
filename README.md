# EmailCleaner

If you have a very cluttered email inbox or a mailbox
overfilled with useless promotion emails,
going through them one by one and deleting them is time-consuming and boring.
That's why to help myself and others, I created this project,
making the deletion of thousands of mail take no more than three clicks.

# Demo

![Project Demo](https://i.imgur.com/7bPqJ57.gif)
> All messages are **PERMANENTLY** deleted and are not moved to trash box!

# How to use

On the project GUI, from left to right, there are three main widgets:

1. Email selection dropdown
2. Option selection dropdown
3. Execute button

**Email selection dropdown**  
This is used to select the organizations or people messagin you.
All emails from them are automatically selected.

**Option selection dropdown**  
This is used to select an options from an option list that
includes the following:

- Scan Inbox - the first and only option, when opening the app,
  after scanning the inbox, more option will appear.
- Delete - this option lets you delete all the mail from a single sender or
  organization, which needs to be selected from the mail selection dropdown.
- Save - this option saves a sender's or organization's mails from batch
  deletion, which needs to be selected from the mail selection dropdown.
- Batch Delete - this option lets you delete all emails from senders or
organizations that are in the mail selection dropdown menu,
except the ones that are saved.
- Clear Saved - this option lets you clear the saved senders making them
  present in the mail selection menu thus making them deletable again.

**Execute Button**  
This button when clicked will execute the command in the option menu dropdown.

> The GUI has a message display field that will give instruction and
> information or error messages, making the project usage more straight forward.

## Outside App Requirements

- Python 3.10.7 or greater
- The pip package management tool
- A Google account with Gmail enabled
- A Google Cloud project

## Managing Gmail API

Follow
these [instructions](https://developers.google.com/gmail/api/quickstart/python#step_1_turn_on_the_api_name).

## Installation

- After completing the Gmail developer account and downloading the json file,
  rename it to credentials.json and put it in the app directory.
- Create a virtual environment.
- Activate the virtual environment.
- Install requirements.txt **(Make sure the virtual environment is activated!)**

## Run The App

- Run main.py

    