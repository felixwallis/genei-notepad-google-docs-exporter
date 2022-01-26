from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/documents']

# The ID of a sample document.
DOCUMENT_ID = '195j9eDD3ccgjQRttHhJPymLJUCOUjs-jmwTrekvdjFE'


def main():
    """Shows basic usage of the Docs API.
    Prints the title of a sample document.
    """
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

    try:
        service = build('docs', 'v1', credentials=creds)

        title = 'My Document'
        body = {
            'title': title
        }

        document = service.documents().create(body=body).execute()
        document_id = document.get('documentId')

        text = '\n\nHobbes defines liberty in two ways: in the state of nature, "Liberty, is understood, according to the proper signification of the word, the absence of externall impedi- ments." \nCivil liberty, under government, is the absence of law or other sovereign commandment. "The Greatest Liberty of Subjects, dependeth on the Silence of the Law."\nBoth accounts make it entirely possible to act voluntarily but from fear, and neither suggests that freedom has anything to do with the freedom of the will. \nIn this definition, Hobbes wanted to enforce the claim thatfreedom was not a matter of form of government. \nFreedom and government are antithetical, because we give up all our rights when we enter political society, savethe right to defend ourselves against the immediate threat of death and injury.'
        requests = [
            {
                'insertText': {
                    'location': {
                        'index': 1,
                    },
                    'text': text
                }
            },
            {
                'updateTextStyle': {
                    'range': {
                        'startIndex': 1,
                        'endIndex': len(text)
                    },
                    'textStyle': {
                        'weightedFontFamily': {
                            'fontFamily': 'Georgia'
                        }
                    },
                    'fields': 'weightedFontFamily'
                }
            }
        ]

        service.documents().batchUpdate(documentId=document_id,
                                        body={'requests': requests}).execute()

        print('Created document with title: {0}'.format(document.get('title')))
    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()
