# Pidgin
 This is a bulk email deleting project, using the Gmail API, made to clear cluttered email inboxes. Providing the following options:

 - Deleting all emails from a perticular sender.
 - Deleting all emails except emails from a list of specific senders.  

## App Workflow

 - ### Load Email Senders  
    Iterates over every email and loads its sender in to the choice box.
    ![load_email](https://i.imgur.com/gNqmZmA.gif)
 - ### Delete
    From the dropdown menu you can view all the people or organizations who have mailed you, after selecting a particular mail sender you can click the delete button to delete all the emails from them.
    ![delete_email](https://i.imgur.com/ceRKqV9.gif)    
 - ### Exclude Delete
    Chose a person or organization you wish to add to the excluded list(emails messages from them are gonna be ignored), then by clicking on the delete button all the mail except the mail from the senders in that list will be deleted.
    ![exclude_delete](https://i.imgur.com/YANQ4zu.gif)


### All messages are **PERMANENTLY** deleted and are not moved to trash box!

 ## Outside App Requirements
  - Python 3.10.7 or greater
  - The pip package management tool  
  - A Google account with Gmail enabled
  - A Google Cloud project    

## Managing Gmail API
Follow these [instructions](https://developers.google.com/gmail/api/quickstart/python#step_1_turn_on_the_api_name).

## Installation

- After completing the Gmail developer account and downloading the json file, rename it to credentials.json and put it in the app directory.
- Create a virtual environment.
- Activate the virtual environment.
- Install requirements.txt **(Make sure the virtual environment is activated!)**

## Run The App
- Activate the virtual environment.
- Run main.py

    