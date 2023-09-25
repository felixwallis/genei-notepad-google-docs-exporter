from dotenv import load_dotenv
import os
import json
import requests

load_dotenv()

API_URL = os.getenv('API_URL')
API_KEY = os.getenv('API_KEY')

if not API_URL or not API_KEY:
    raise ValueError("API_URL or API_KEY is missing in environment variables.")

HEADERS = {
    'Content-Type': 'application/json',
    'x-api-key': API_KEY
}


def handle_request_errors(func):
    """Decorator to handle common request errors."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.RequestException as err:
            print(f"Request error: {err}")
            return None
        except json.JSONDecodeError:
            print("Error decoding JSON from response.")
            return None
        except KeyError:
            print("Expected key not found in response.")
            return None
    return wrapper


@handle_request_errors
def search_notes(note_name: str) -> str:
    search_query = f"""
        query {{
            searchByName(input: {{
                name: "{note_name}"
            }}) {{
                results {{
                    item {{
                        __typename
                        ... on Note {{
                            id
                            name
                        }}
                    }}
                    score
                }}
            }}
        }}
    """
    response = requests.post(
        API_URL, json={'query': search_query}, headers=HEADERS)
    response.raise_for_status()

    search_results = response.json()['data']['searchByName']['results']

    if 'errors' in response.json():
        print("GraphQL Error:", response.json()['errors'])
        return None

    return search_results[0]['item']['id'] if search_results else None


@handle_request_errors
def fetch_note_json(note_name):
    note_id = search_notes(note_name)

    if not note_id:
        return f'No note found with name "{note_name}". Please try a different search term.'

    data_query = f"""
        query {{
            note(id: "{note_id}") {{
                data
            }}
        }}
    """
    response = requests.post(
        API_URL, json={'query': data_query}, headers=HEADERS)
    response.raise_for_status()

    note_json = response.json()['data']['note']['data']['root']

    if 'errors' in response.json():
        print("GraphQL Error:", response.json()['errors'])
        return {}

    return note_json


if __name__ == '__main__':
    note_name = input('Enter the name of the note you want to fetch: ')
    note_json = fetch_note_json(note_name)
    if not note_json:
        print('No note found with that name.')
    else:
        print(json.dumps(note_json, indent=2))
