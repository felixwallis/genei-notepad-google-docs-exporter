import requests
import json


def search_genei_notes(input):
    query = '''query {
        searchByName(input: {
            name: "''' + input + '''"
        }) {
            results {
                item {
                    __typename
                    ... on Note {
                        id
                        name
                    }
                }
                score
            }
        }
    }'''
    url = 'https://dev.api.app.genei.io/graphql'
    headers = {'Content-Type': 'application/json', 'x-api-key': 'sk_12f9accc6ff84c23a9cd1a67818fab0b'}
    r = requests.post(url, json=({'query': query}), headers=headers)
    return r.json()

search_results = search_genei_notes('test')
top_search_result = search_results['data']['searchByName']['results'][0]
top_search_result_id = top_search_result['item']['id']

def get_note_data(input):
    query = '''query {
        note(id: "''' + input + '''") {
            data
        }
    }'''
    url = 'https://dev.api.app.genei.io/graphql'
    headers = {'Content-Type': 'application/json', 'x-api-key': 'sk_12f9accc6ff84c23a9cd1a67818fab0b'}
    r = requests.post(url, json=({'query': query}), headers=headers)
    return r.json()

note_data = get_note_data(top_search_result_id)
print(note_data)