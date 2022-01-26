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

        text = '\n\n-Hobbes\'s most famous single phrase is his observation that life in the state of nature is "solitary, poore, nasty, brutish, and short."\n-Hobbes dissented from Aristotle on the substance of human nature.\n-Aristotle thought that there was some kind of natural attraction toward the good, and toward life in society. Hobbes thinks that at best there is a common aversion to the summum malum, or death, and that we become "apt" for soci- ety only by being socialized into decent conduct.\n-Equally important is Hobbes\'s insistence on the natural equality of man- kind. Thinking of humanity as morally, politically, and intellectually on a level reinforced the view that the state rested on universal consent rather than on a tendency toward a natural hierarchy.\n-Hobbes says the heads of all governments live in a state of nature with respect to one another.\n-The state of nature is simply the condition where we are forced into contact with each other in the absence of a superior authority that can lay down and enforce rules to govern our behavior toward each other.\n-The state of nature with which Hobbes is concerned is more nearly the condition of civilized people deprived of stable govern- ment than anything else.'
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
