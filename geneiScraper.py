from bs4 import BeautifulSoup
import xmltojson
import json
import re


# with open('genei_notepad.html', 'r') as html_file:
#     html = html_file.read()
#     json_ = xmltojson.parse(html)
# with open('data.json', 'w') as file:
#     json.dump(json_, file)

h1_text = []
h2_text = []
h3_text = [h1_text]


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
            all_text_string += text
        for h1_element in h1_elements:
            h1_text.append(h1_element.get_text())
        for h2_element in h2_elements:
            h2_text.append(h2_element.get_text())
        for h3_element in h3_elements:
            h3_text.append(h3_element.get_text())


def get_header_positions():
    for header in h1_text:
        rl = re.split(r'\s', header)
        print(rl)


get_headers()
get_header_positions()
