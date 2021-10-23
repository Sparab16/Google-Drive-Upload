from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly',
          'https://www.googleapis.com/auth/drive.file']


def authentication():
    """
    Shows the basic usage of the drive v3 API.
    @return: return the service object
    """
    try:
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        service = build('drive', 'v3', credentials=creds)
        return service
    except Exception as e:
        raise Exception(e)

def create_folder(service, folder_to_create):
    """
    Function is responsible for creating (if not exists) folder in the G drive
    @param service: API object
    @param folder_to_create: Name of the folder to create
    @return: ID of the created/existing folder
    """
    try:
        response = service.files().list(q="mimeType='application/vnd.google-apps.folder'",
                                        spaces='drive',
                                        fields='nextPageToken, files(id, name)',
                                        ).execute()

        for file in response.get('files', []):
            # Condition to check whether the folder with that name already exists in Gdrive
            if file.get('name') == folder_to_create:
                return file.get('id')

        # If Folder with that name is not present inside the google drive
        file_metadata = {
            'name': folder_to_create,
            'mimeType': 'application/vnd.google-apps.folder'
        }

        file = service.files().create(body=file_metadata, fields='id').execute()
        return file.get('id')
    except Exception as e:
        raise Exception(e)

def upload(service, folder_id, files_to_upload, textarea, root):
    """
    Function is responsible for uploading the files to Gdrive
    @param service: Drive API object
    @param folder_id: ID of the parent folder
    @param files_to_upload: Array of files which is to be uploaded
    @return: Boolean value whether upload is successful(True) or not(False)
    """
    try:
        textarea['state'] = 'normal'
        textarea.insert('end', '------------------------UPLOADING STARTED----------------------\n')
        root.update_idletasks()
        file_counter = len(files_to_upload)
        for file in files_to_upload:
            # Setting meta data for the files
            file_metadata = {
                'name': file.split('/')[-1],
                'parents': [folder_id]
            }
            # Setting content of file to upload
            media = MediaFileUpload(file, resumable=True)
            # Uploading the files
            file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            # Updating the textarea with uploaded file
            root.update_idletasks()
            textarea.insert('end', 'File : ' + str(file_counter) + ' = ' + file_metadata[
                'name'] + ' has been uploaded to Google Drive.\n')
            textarea.see('end')
            root.update_idletasks()
            file_counter -= 1

        textarea.insert('end', '------------------------UPLOADING ENDED----------------------\n')
        textarea['state'] = 'disabled'
        return True
    except Exception as e:
        return False

