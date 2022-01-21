from bs4 import BeautifulSoup
import re
from operator import itemgetter


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
    header_positions = {}
    for header in h1_text:
        header_position = all_text_string.index(header)
        header_position_pair = {
            header: header_position
        }
        header_positions.update(header_position_pair)
    for header in h2_text:
        header_position = all_text_string.index(header)
        header_position_pair = {
            header: header_position
        }
        header_positions.update(header_position_pair)
    for header in h3_text:
        header_position = all_text_string.index(header)
        header_position_pair = {
            header: header_position
        }
        header_positions.update(header_position_pair)
    global sorted_header_positions
    sorted_header_positions = dict(
        sorted(header_positions.items(), key=lambda item: item[1]))


get_headers()
get_header_positions()
