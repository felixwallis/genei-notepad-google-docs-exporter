from bs4 import BeautifulSoup
import re
import json
import openai
import google_docs_formatting_helpers
import google_docs_api_helpers


# Convert text in genei_notepad.html to string
def get_all_text(all_text):
    # Store text string globally for future functions
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


# Return all headers of a given type as an array
def create_header_arrays(header_elements):
    header_text = []
    for header_element in header_elements:
        words = re.split(r'\s', header_element.get_text())
        words_in_header = []
        for word in words:
            if len(word):
                words_in_header.append(word)
        header = ' '.join(words_in_header)
        header_text.append(header)

    return header_text


# Return index position of a specific header in all_text_string
# Complexity is added by handling duplicate headers
def get_header_position(header, header_type, h3_present, header_previous_occurance_position=None):
    if header_previous_occurance_position == None:
        header_index = all_text_string.index(header)
    else:
        text_to_search = all_text_string[header_previous_occurance_position + len(header):
                                         len(all_text_string)]
        header_index = text_to_search.index(
            header) + (len(all_text_string) - len(text_to_search))

    return {
        'header': header,
        'header_position': header_index,
        'header_type': header_type,
        'h3_present': h3_present
    }


# Return index positions of all headers of a given type in all_text_string
# Complexity is added by handling duplicate headers
def get_header_positions(headers, header_type, h3_present):
    type_specific_header_positions = []
    headers_dict = {}
    for index, header in enumerate(headers):
        try:
            headers_dict[header].append(index)
        except:
            headers_dict[header] = [index]

        header_occurance_array = headers_dict[header]
        if len(header_occurance_array) == 1:
            type_specific_header_positions.append(get_header_position(
                header, header_type, h3_present))
        elif len(header_occurance_array) > 1:
            header_previous_occurance_index = header_occurance_array[len(
                header_occurance_array)-2]
            header_previous_occurance_position = type_specific_header_positions[
                header_previous_occurance_index]['header_position']
            type_specific_header_positions.append(get_header_position(
                header, header_type, h3_present, header_previous_occurance_position))

    return type_specific_header_positions


# Return text between two headers from all_text_string
def retrieve_text_between_markers(marker_1, marker_2, header_length):
    text_snippet = ''
    for index, char in enumerate(all_text_string):
        if marker_2 is not None:
            if index >= (marker_1 + header_length) and index < marker_2:
                text_snippet += char
        else:
            if index >= (marker_1 + header_length):
                text_snippet += char

    if len(text_snippet):
        text_snippet_obj = {
            'text': text_snippet,
            'text_type': 'unstyled'
        }
        return text_snippet_obj


# Return genei_notepad.html outline based on headers, header positions, and text between headers
def generate_text_snippets(header_positions):
    document_outline = []
    for index, header_position in enumerate(header_positions):
        marker_1 = header_position['header_position']
        if index < len(header_positions) - 1:
            marker_2 = header_positions[index + 1]['header_position']
        else:
            marker_2 = None

        # Retrieve text before first header if it exists
        if index == 0 and marker_1 != 0:
            document_outline.append(retrieve_text_between_markers(
                0, marker_1, 0))

        header = {
            'text': header_position['header'],
            'text_type': header_position['header_type'],
            'h3_present': header_position['h3_present']
        }
        document_outline.append(header)

        text_between_headers = retrieve_text_between_markers(
            marker_1, marker_2, len(header_position['header']))
        if text_between_headers:
            document_outline.append(text_between_headers)

    return document_outline


# Return JSON object from generic GPT-3 request
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


# Return a text string turned into bullet points by GPT-3
def process_text_snippet_with_openai(text_to_process):
    text_prompt = 'Turn these sentences into bullet points: ' + \
        text_to_process
    processed_text = make_openai_request(
        text_prompt, 'text-davinci-001')['choices'][0]['text']
    # Long processed_text indicates successful processing by GPT-3
    if len(processed_text) > (len(text_to_process) * 0.5):
        return processed_text
    else:
        print('Poor GPT-3 response. Reprocessing text element...')
        new_text_prompt = 'Turn these sentences into a paragraph: ' + text_to_process
        processed_paragraph = make_openai_request(
            new_text_prompt, 'text-davinci-001')['choices'][0]['text']
        # Split paragraph at periods and add new lines to turn into bullet points later
        reprocessed_text = []
        for sentence in processed_paragraph.split('. '):
            if '\n' in sentence:
                reprocessed_text.append(sentence)
            else:
                new_line = '\n' + sentence
                reprocessed_text.append(new_line)
        return '. '.join(reprocessed_text)


# Return updated document_outline with text snippets processed using GPT-3
def process_document_outline(document_outline):
    with open('../openai_credentials.json', 'r') as fp:
        json_data = json.load(fp)
        openai.api_key = json_data['API_Key']

    processed_document_outline = []
    for index, text_element in enumerate(document_outline):
        if text_element['text_type'] == 'unstyled':
            # Check length of text to be processed does not exceed GPT-3 token limit
            if (len(text_element['text'])/4) < 1048:
                text_element['processed_text'] = process_text_snippet_with_openai(
                    text_element['text'])
                processed_document_outline.append(text_element)
            elif (len(text_element['text'])/4) > 2048:
                print('The following text snippet is too long for GPT-3 processing. Add a heading or subheading to split this snippet into smaller sections: ',
                      '\n', text_element['text'])
        else:
            processed_document_outline.append(text_element)
        print('Processed text element', (index + 1),
              'of', len(document_outline))

    return processed_document_outline


# Example of document outline processed by GPT-3
# Only use when testing
def premade_processed_document_outline():
    with open('../example_processed_text.json', 'r') as fp:
        json_data = json.load(fp)
        processed_document_outline = json_data['processed_document_outline']

    return processed_document_outline


# Fix any weird carriage returns added by GPT-3
def correct_carriage_returns(text):
    first_four_chars = text[:3]
    if '\n\n' in first_four_chars:
        return text[2:]
    else:
        return text


# Write the GPT-3 processed document_outline to a Google Docs file
def covert_document_outline_to_google_doc(title, processed_document_outline):
    document_id = google_docs_api_helpers.create_document(title)
    for text_item in reversed(processed_document_outline):
        text_type = text_item['text_type']
        if text_type == 'unstyled':
            processed_text = text_item['processed_text']
            text_without_spaces_after_bulletpoints = processed_text.replace(
                '\n- ', '\n')
            text_without_all_bullet_points = text_without_spaces_after_bulletpoints.replace(
                '\n-', '\n')
            text_with_cleaned_hyphens = text_without_all_bullet_points.replace(
                '- ', '')
            text_with_corerct_spacing = re.sub(r'\.(?=\S)([A-Z])', ('. ' + r'\1'),
                                               text_with_cleaned_hyphens)
            cleaned_text = correct_carriage_returns(text_with_corerct_spacing)
            requests = google_docs_formatting_helpers.create_text_with_bullet_points(
                cleaned_text)
            google_docs_api_helpers.update_document(requests, document_id)
        else:
            header = text_item['text']
            h3_present = text_item['h3_present']
            if text_type == 'h1' and h3_present:
                requests = google_docs_formatting_helpers.create_bold_header(
                    header)
                google_docs_api_helpers.update_document(
                    requests, document_id)
            elif text_type == 'h2' and h3_present:
                requests = google_docs_formatting_helpers.create_header(
                    header)
                google_docs_api_helpers.update_document(
                    requests, document_id)
            elif text_type == 'h3':
                requests = google_docs_formatting_helpers.create_bold_sub_header(
                    header)
                google_docs_api_helpers.update_document(
                    requests, document_id)
            elif text_type == 'h1' and h3_present == False:
                requests = google_docs_formatting_helpers.create_header(
                    header)
                google_docs_api_helpers.update_document(
                    requests, document_id)
            elif text_type == 'h2' and h3_present == False:
                requests = google_docs_formatting_helpers.create_bold_sub_header(
                    header)
                google_docs_api_helpers.update_document(
                    requests, document_id)
    requests = google_docs_formatting_helpers.create_title(title)
    google_docs_api_helpers.update_document(
        requests, document_id)


def export_genei_notepad_to_google_doc():
    print('Give this document a name: ')
    title = input()

    print('Scraping content...')

    with open('../genei_notepad.html') as fp:
        soup = BeautifulSoup(fp, 'html.parser')
        get_all_text(soup.find_all(text=True))
        h1_headers = create_header_arrays(soup.find_all('h1'))
        h2_headers = create_header_arrays(soup.find_all('h2'))
        h3_headers = create_header_arrays(soup.find_all('h3'))

    # Check if h3 headers are present for Google Drive formatting
    if len(h3_headers):
        h3_present = True
    else:
        h3_present = False

    print('Getting header positions...')
    header_positions = []
    for header_position in get_header_positions(h1_headers, 'h1', h3_present):
        header_positions.append(header_position)
    for header_position in get_header_positions(h2_headers, 'h2', h3_present):
        header_positions.append(header_position)
    for header_position in get_header_positions(h3_headers, 'h3', h3_present):
        header_positions.append(header_position)

    header_positions.sort(
        key=lambda item: item['header_position'])

    print('Generating document outline...')
    document_outline = generate_text_snippets(header_positions)

    print('Processing document outline...')
    processed_document_outline = process_document_outline(document_outline)
    # Use this premade processed document outline when testing to prevent being
    # charged for GPT-3 use
    # processed_document_outline = premade_processed_document_outline()

    print('Coverting document outline to Google Doc...')
    covert_document_outline_to_google_doc(title, processed_document_outline)


if __name__ == '__main__':
    export_genei_notepad_to_google_doc()
