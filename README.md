# Pidgin

## About this Project
 This is a bulk email deleting project made to clear cluttered email inboxes. Providing the following options:

 - Deleting all emails from a perticular sender.
 - Deleting all emails except emails from a list of specific senders  
**WARNING: Messages will be PERMANENTLY deleted!!**

## App Workflow

 - ### Load Email Senders  
    > Loads all emails, and gets their senders.
  ![load_email](https://i.imgur.com/gNqmZmA.gif)
 - ### Delete
   > From the dropdown you can select from all the people or organizations mailing you, after that clicking on delete will delete all the mail, they have sent.
  ![delete_email](https://i.imgur.com/ceRKqV9.gif)    
 - ### Exclude Delete
    > Chose a person or organization you wish to ignore, after that you can ignore more or click on delete witch will delete all the mail except the previously selected ones.
    ![exclude_delete](https://i.imgur.com/YANQ4zu.gif)

 ## Outside App Requirements
  - Python 3.10.7 or greater
  - The pip package management tool  
  - A Google account with Gmail enabled
  - A Google Cloud project    

## Managing Gmail API
Follow these [instructions](https://developers.google.com/gmail/api/quickstart/python#step_1_turn_on_the_api_name).

## Installation

- Put the json file, you got after making the google dev account, in to the app directory and rename it to credentials.json
- Create a virtual environment:
- Install requirements.txt.

## Run The App
- Activate the virtual environment.
- Run main.py file

    