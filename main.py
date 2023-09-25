import os
import json

from tqdm import tqdm

from clients.fetch_note_json import fetch_note_json
from conversion.json_to_md import json_to_md


def load_config(config_path='config.json'):
    """
    Loads the configuration file.
    """
    with open(config_path, 'r') as file:
        return json.load(file)


def convert_note_to_markdown(note_name: str):
    """
    Fetches Genei note JSON and converts it to markdown format.
    """
    note_json = fetch_note_json(note_name)
    if not note_json:
        print(f'No note found with the name: {note_name}')
        return None

    markdown_output = json_to_md(note_json)
    assert markdown_output, 'Conversion resulted in empty markdown output'
    return markdown_output


def save_markdown_output(markdown_output: str,
                         note_name: str,
                         dist_dir_path: str):
    """
    Saves markdown output to a file.
    """
    if not os.path.exists(dist_dir_path):
        os.makedirs(dist_dir_path)

    file_path = os.path.join(dist_dir_path, f"{note_name}.md")
    with open(file_path, 'w') as file:
        file.write(markdown_output)


def main():
    config = load_config()

    try:
        with open(config["note_names_file_path"], 'r') as file:
            note_names = file.readlines()

        for note_name in tqdm(note_names, desc="Converting notes", unit="note"):
            note_name = note_name.strip()
            if not note_name:
                continue

            markdown_output = convert_note_to_markdown(note_name)

            if markdown_output:
                save_markdown_output(
                    markdown_output, note_name, config["dist_dir_path"])

    except FileNotFoundError:
        print(f"Error: File {config['note_names_file_path']} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    main()
