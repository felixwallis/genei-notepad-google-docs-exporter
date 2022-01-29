from urllib import response
from bs4 import BeautifulSoup
import re
import json
import openai
import google_docs_formatting_helpers
import google_docs_api_helpers

print('Give this document a name: ')
title = input()

h1_text = []
h2_text = []
h3_text = []


def get_headers():
    print('Retrieving headers...')

    with open('genei_notepad.html') as fp:
        soup = BeautifulSoup(fp, 'html.parser')
        all_text = soup.find_all(text=True)
        h1_elements = soup.find_all('h1')
        h2_elements = soup.find_all('h2')
        h3_elements = soup.find_all('h3')
        global all_text_string
        all_text_string = ''
        for text in all_text:
            all_text_list = []
            rl = re.split(r'\s', text)
            for word in rl:
                if len(word):
                    all_text_list.append(word)
            text = ' '.join(all_text_list)
            all_text_string += text
        for h1_element in h1_elements:
            h1_text_list = []
            rl = re.split(r'\s', h1_element.get_text())
            for word in rl:
                if len(word):
                    h1_text_list.append(word)
            header = ' '.join(h1_text_list)
            h1_text.append(header)
        for h2_element in h2_elements:
            h2_text_list = []
            rl = re.split(r'\s', h2_element.get_text())
            for word in rl:
                if len(word):
                    h2_text_list.append(word)
            header = ' '.join(h2_text_list)
            h2_text.append(header)
        for h3_element in h3_elements:
            h3_text_list = []
            rl = re.split(r'\s', h3_element.get_text())
            for word in rl:
                if len(word):
                    h3_text_list.append(word)
            header = ' '.join(h3_text_list)
            h3_text.append(header)


def get_header_positions():
    print('Getting header positions...')

    global header_positions
    header_positions = []
    if len(h3_text):
        h3_present = True
    else:
        h3_present = False
    for header in h1_text:
        header_position = all_text_string.index(header)
        header_info = {
            'header': header,
            'header_position': header_position,
            'header_type': 'h1',
            'h3_present': h3_present
        }
        header_positions.append(header_info)
    for header in h2_text:
        header_position = all_text_string.index(header)
        header_info = {
            'header': header,
            'header_position': header_position,
            'header_type': 'h2',
            'h3_present': h3_present
        }
        header_positions.append(header_info)
    for header in h3_text:
        header_position = all_text_string.index(header)
        header_info = {
            'header': header,
            'header_position': header_position,
            'header_type': 'h3',
            'h3_present': h3_present
        }
        header_positions.append(header_info)

    header_positions.sort(
        key=lambda item: item['header_position'])


def retrieve_text_between_markers(marker_1, marker_2, header_length):
    text_snippet = ''
    for index, char in enumerate(all_text_string):
        if marker_2 is not None:
            if index >= (marker_1 + header_length) and index < marker_2:
                text_snippet += char
        else:
            if index >= (marker_1 + header_length):
                text_snippet += char
    return text_snippet


def generate_text_snippets():
    print('Generating text snippets...')

    global document_outline
    document_outline = []
    for index, header_position in enumerate(header_positions):
        header = {
            'text': header_position['header'],
            'text_type': header_position['header_type'],
            'h3_present': header_position['h3_present']
        }
        document_outline.append(header)

        marker_1 = header_position['header_position']
        if index < len(header_positions) - 1:
            marker_2 = header_positions[index + 1]['header_position']
        else:
            marker_2 = None
        text_snippt = retrieve_text_between_markers(
            marker_1, marker_2, len(header_position['header']))
        text_after_header = {
            'text': text_snippt,
            'text_type': 'unstyled'
        }
        document_outline.append(text_after_header)


def make_openai_request(text_prompt, model):
    response = openai.Completion.create(
        engine=model,
        prompt=text_prompt,
        temperature=0.7,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0.5,
        presence_penalty=0.2
    )
    json_object = json.loads(str(response))

    return json_object


def process_document_with_openai():
    print('Processing text snippets...')

    api_key = ''
    with open('OpenAI_API_Key.json', 'r') as fp:
        json_data = json.load(fp)
        api_key = json_data['API_Key']
    openai.api_key = api_key

    global processed_document_outline
    processed_document_outline = []
    for text_element in document_outline:
        if text_element['text_type'] == 'unstyled':
            text_prompt = 'Turn these sentences into bullet points: ' + \
                text_element['text']
            processed_text = make_openai_request(
                text_prompt=text_prompt, model='text-davinci-001')['choices'][0]['text']
            if len(processed_text) > (len(text_element['text']) * 0.8):
                text_element['processed_text'] = processed_text
            else:
                new_text_prompt = 'Turn these sentences into a paragraph: ' + \
                    text_element['text']
                processed_paragraph = make_openai_request(
                    text_prompt=new_text_prompt, model='text-davinci-001')['choices'][0]['text']
                reprocessed_text_list = []
                for sentence in processed_paragraph.split('. '):
                    if '\n' not in sentence:
                        bullet_point = '\n' + sentence
                        reprocessed_text_list.append(bullet_point)
                    else:
                        reprocessed_text_list.append(sentence)
                text_element['processed_text'] = '.'.join(
                    reprocessed_text_list)
            processed_document_outline.append(text_element)
        else:
            processed_document_outline.append(text_element)

    # with open('dev_processed_text.json', 'r') as fp:
    #     json_data = json.load(fp)
    #     processed_document_outline = json_data['processed_document_outline']


def add_outline_to_google_doc():
    document_id = google_docs_api_helpers.create_document(title)
    for text_item in reversed(processed_document_outline):
        if text_item['text_type'] == 'unstyled':
            text_without_spaced_bullet_points = text_item['processed_text'].replace(
                '\n- ', '\n')
            text_without_all_bullet_points = text_without_spaced_bullet_points.replace(
                '\n-', '\n')
            text_with_cleaned_hyphens = text_without_all_bullet_points.replace(
                '- ', '')
            cleaned_text = re.sub(r'\.(?=\S)([A-Z])', ('. ' + r'\1'),
                                  text_with_cleaned_hyphens)
            requests = google_docs_formatting_helpers.create_text_with_bullet_points(
                cleaned_text)
            google_docs_api_helpers.update_document(
                requests=requests, document_id=document_id)
        elif text_item['text_type'] == 'h1' and text_item['h3_present']:
            header = '\n\n' + text_item['text']
            requests = google_docs_formatting_helpers.create_bold_header(
                header)
            google_docs_api_helpers.update_document(
                requests=requests, document_id=document_id)
        elif text_item['text_type'] == 'h2' and text_item['h3_present']:
            header = '\n\n' + text_item['text']
            requests = google_docs_formatting_helpers.create_header(header)
            google_docs_api_helpers.update_document(
                requests=requests, document_id=document_id)
        elif text_item['text_type'] == 'h3':
            header = '\n\n' + text_item['text']
            requests = google_docs_formatting_helpers.create_bold_sub_header(
                header)
            google_docs_api_helpers.update_document(
                requests=requests, document_id=document_id)
        elif text_item['text_type'] == 'h1' and text_item['h3_present'] != True:
            header = '\n\n' + text_item['text']
            requests = google_docs_formatting_helpers.create_header(header)
            google_docs_api_helpers.update_document(
                requests=requests, document_id=document_id)
        elif text_item['text_type'] == 'h2' and text_item['h3_present'] != True:
            header = '\n\n' + text_item['text']
            requests = google_docs_formatting_helpers.create_bold_sub_header(
                header)
            google_docs_api_helpers.update_document(
                requests=requests, document_id=document_id)
    requests = google_docs_formatting_helpers.create_title(title)
    google_docs_api_helpers.update_document(
        requests=requests, document_id=document_id)


get_headers()
get_header_positions()
generate_text_snippets()
process_document_with_openai()
add_outline_to_google_doc()
