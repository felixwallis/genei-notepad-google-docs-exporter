# genei-notepad-google-docs-exporter (GNGDE)
GNGDE is a python script for ‘smartly’ exporting Genei notepads to Google Docs. It uses [OpenAI’s GPT-3 autoregressive language model](https://openai.com/blog/gpt-3-apps/) to summarise, punctuate, and format Genei notepad content and create a Google Doc based on its output. 

## GNGDE solves two problems with Genei notepads
Notes become messy and disorganised when adding highlighted text and summaries to a Genei notepad. They quickly become full of lousy punctuation, grammatical errors, and inconsistent formatting. Fixing these problems is time-consuming and tedious. GNGDE solves this problem by using GPT-3 to process notepad content and fix its formatting, punctuation, and grammar. GPT-3 can also summarise Genei notepads, distilling extended highlights from PDFs or lengthy summaries. 

A further problem with Genei notepads is that they currently do not have any GSuite export options. GNGDE performs this task by writing GPT-3 processed content to Google Docs. 

# Setup
## Packages
GNGDE uses the packages outlined in the [requirements.txt](requirements.txt) file. Run `pip install -r requirements.txt` to install these packages on your local machine.

## OpenAI API
GNGDE requires an OpenAI API key which can be accessed [here](https://beta.openai.com/account/api-keys). Paste your API key into the `API_Key` field in the [openai_credentials.json](openai_credentials.json) file.

## Google Docs API
GNGDE uses the [Google Docs API](https://developers.google.com/docs/api). Google Docs API credentials can be generated via the following steps. 
1. Create a new project in the [Google Cloud Console](https://console.cloud.google.com/).
2. [Enable the Google Docs API](https://console.cloud.google.com/apis/library/docs.googleapis.com) for your project from the Google Cloud Console. 
3. Create credentials for the Google Docs API:
    - Visit the Enabled APIs and services tab in the Google Cloud Console, select the Google Docs API, and click the Create Credentials button. 
    - GNGDE requires access to user data, so choose this option when choosing a credential type. 
    - Fill in the OAuth consent screen page using the app name genei-notepad-google-docs-exporter. 
    - Use your email for the user support email and developer contact information fields. 
    - Enable the ./auth/documents scope for the OAuth credential so GNGDE can create and edit Google Docs. 
    - Select ‘Desktop app’ as the application type for the OAuth Client ID and give the OAuth 2.0 Client a name. 
4. After creating an OAuth 2.0 Client, visit the Credentials tab in the Google Cloud Console and download the OAuth credentials as a .JSON file. Copy and paste the credentials from this file into GNGDE’s [google_docs_credentials.json](google_docs_credentials.json) file. The file should look like this:
`{
  "installed": {
    "client_id": ***,
    "project_id": ***,
    "auth_uri": ***,
    "token_uri": ***,
    "auth_provider_x509_cert_url": ***,
    "client_secret": ***,
    "redirect_uris": [***]
  }
}`
5. To ensure you have access to GNGDE, visit the OAuth consent screen tab in the Google Cloud Console and add your email as a test user under the Test users section. 

# Usage
## Retrieving content from the Genei notepad
1. Using a browser like Chrome, right-click on a Genei notepad to inspect its elements and find the div with the ID `genei-editor-container`. 
2. Copy all of this div’s child elements. This can be done in Chrome by right-clicking on the div, selecting ‘Edit as HTML’ and copying all the editable content. 
3. Paste this HTML into GNGDE’s [genei_notepad.html](genei_notepad.html) file. 

## Running GNGDE
1. Run the [export_genei_notepad.py](export_genei_notepad.py) file in GNGDE’s export_genei_notepad directory.
2. When first running the [export_genei_notepad.py](export_genei_notepad.py) file, the Google Docs API will ask for GNGDE to be authorised. Follow Google’s authentication flow to authorise the app. 
3. Visit your Google Drive to view your ‘smart’ Genei notepad export as a Google Doc!

## Fine-tuning
- GPT-3 can process Genei notepad content in various ways by changing the `text_prompt` variable in the `process_text_snippet_with_openai` function in the [export_genei_notepad.py](export_genei_notepad.py) file. By default, this prompt is set to ‘Turn these sentences into bullet points: ’ but can be changed according to how you would like the model to process your notepad. 
- GPT-3’s response can also be tuned by editing the `temperature`, `frequency_penalty`, and `presence_penalty` fields in the `openai.Completion.create()` method called by the `make_openai_request` function in the [export_genei_notepad.py](export_genei_notepad.py) file. 
- GNGDE’s Google Docs formatting can be edited by changing the `requests` arrays in the `create_title`, `create_bold_header`, `create_header`, `create_bold_sub_header`, and `create_text_with_bullet_points` functions in the [google_docs_formatting_helpers.py](google_docs_formatting_helpers.py) file. 

# Support
If you have any problems or troubleshooting queries when using GNGDE, please open a new issue in the GitHub repo, and I’ll make sure to reply to it as soon as possible 😃.

# Contributing
Pull requests are welcome. For significant changes, please open an issue first to discuss what you would like to change.

# Licence
[MIT](https://choosealicense.com/licenses/mit/)







