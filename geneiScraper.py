from urllib import response
from bs4 import BeautifulSoup
import re
import json
import openai


h1_text = []
h2_text = []
h3_text = []


def get_headers():
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
    global header_positions
    header_positions = []
    for header in h1_text:
        header_position = all_text_string.index(header)
        header_info = {
            'header': header,
            'header_position': header_position,
            'header_type': 'h1'
        }
        header_positions.append(header_info)
    for header in h2_text:
        header_position = all_text_string.index(header)
        header_info = {
            'header': header,
            'header_position': header_position,
            'header_type': 'h2'
        }
        header_positions.append(header_info)
    for header in h3_text:
        header_position = all_text_string.index(header)
        header_info = {
            'header': header,
            'header_position': header_position,
            'header_type': 'h3'
        }
        header_positions.append(header_info)

    header_positions.sort(
        key=lambda item: item['header_position'])


def retrieve_text_between_markers(marker_1, marker_2, header_length):
    text_snippit = ''
    for index, char in enumerate(all_text_string):
        if marker_2 is not None:
            if index >= (marker_1 + header_length) and index < marker_2:
                text_snippit += char
        else:
            if index >= (marker_1 + header_length):
                text_snippit += char
    return text_snippit


def generate_text_snippits():
    global document_outline
    document_outline = []
    for index, header_position in enumerate(header_positions):
        header = {
            'text': header_position['header'],
            'text_type': header_position['header_type']
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


def process_document_with_openai():
    api_key = ''
    with open('OpenAI_API_Key.json', 'r') as fp:
        json_data = json.load(fp)
        api_key = json_data['API_Key']
    openai.api_key = api_key

    processed_document_outline = []
    base_prompt = 'Turn these sentences into bullet points: '
    for text in document_outline:
        if text['text_type'] == 'unstyled':
            text_prompt = base_prompt + text['text']
            response = openai.Completion.create(
                engine="text-davinci-001",
                prompt=text_prompt,
                temperature=0.7,
                max_tokens=1000,
                top_p=1,
                frequency_penalty=0.5,
                presence_penalty=0.2
            )
            json_object = json.loads(str(response))
            print(json_object['choices'][0]['text'])
            text['processed_text'] = json_object['choices'][0]['text']
            processed_document_outline.append(text)
        else:
            processed_document_outline.append(text)


get_headers()
get_header_positions()
generate_text_snippits()
process_document_with_openai()
