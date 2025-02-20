import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


class CloudSync:
    def __init__(self):
        self.credentials = None
        self.service = None
        self._initialize_google_drive()

    def _initialize_google_drive(self):
        try:
            creds_file = 'credentials.json'  # Path to your Google Drive API credentials
            self.credentials = service_account.Credentials.from_service_account_file(creds_file)
            self.service = build('drive', 'v3', credentials=self.credentials)
            print("Connected to Google Drive.")
        except Exception as e:
            print(f"Failed to connect to Google Drive: {e}")

    def upload_file(self, file_path, folder_id=None):
        file_metadata = {'name': os.path.basename(file_path)}
        if folder_id:
            file_metadata['parents'] = [folder_id]

        media = MediaFileUpload(file_path, resumable=True)
        file = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(f"Uploaded {file_path} to Google Drive with ID: {file.get('id')}")

    def download_file(self, file_id, save_path):
        request = self.service.files().get_media(fileId=file_id)
        with open(save_path, 'wb') as f:
            f.write(request.execute())
        print(f"Downloaded file to {save_path}.")

    def list_files(self, folder_id=None):
        query = f"'{folder_id}' in parents" if folder_id else None
        results = self.service.files().list(q=query, fields="files(id, name)").execute()
        return results.get('files', [])