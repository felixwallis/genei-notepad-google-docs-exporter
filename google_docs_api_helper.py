from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/documents']


def create_document(title):
    global creds
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
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

    try:
        service = build('docs', 'v1', credentials=creds)
        title = title
        body = {
            'title': title
        }
        doc = service.documents().create(body=body).execute()
        print('Created document with title: {0}'.format(doc.get('title')))
        return doc.get('documentId')

    except HttpError as err:
        print(err)


def update_document(requests, document_id):
    try:
        service = build('docs', 'v1', credentials=creds)
        service.documents().batchUpdate(documentId=document_id,
                                        body={'requests': requests}).execute()
    except HttpError as err:
        print(err)
