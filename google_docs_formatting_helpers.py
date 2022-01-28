def create_title(title):
    requests = [
        {
            'insertText': {
                'location': {
                    'index': 1,
                },
                'text': title
            }
        },
        {
            'updateParagraphStyle': {
                'range': {
                    'startIndex': 1,
                    'endIndex': len(title) + 1
                },
                'paragraphStyle': {
                    'namedStyleType': 'TITLE',
                    'alignment': 'CENTER',
                    'lineSpacing': '100'
                },
                'fields': '*'
            }
        },
        {
            'updateTextStyle': {
                'range': {
                    'startIndex': 1,
                    'endIndex': len(title) + 1
                },
                'textStyle': {
                    'weightedFontFamily': {
                        'fontFamily': 'Georgia'
                    },
                    'fontSize': {
                        'magnitude': 18,
                        'unit': 'PT'
                    },
                },
                'fields': 'weightedFontFamily, fontSize'
            }
        }
    ]
    return requests


def create_bold_header(header):
    requests = [
        {
            'insertText': {
                'location': {
                    'index': 1,
                },
                'text': header
            }
        },
        {
            'updateTextStyle': {
                'range': {
                    'startIndex': 1,
                    'endIndex': len(header) + 1
                },
                'textStyle': {
                    'weightedFontFamily': {
                        'fontFamily': 'Georgia'
                    },
                    'fontSize': {
                        'magnitude': 14,
                        'unit': 'PT'
                    },
                },
                'fields': 'weightedFontFamily, fontSize'
            }
        },
        {
            'updateTextStyle': {
                'range': {
                    'startIndex': 1,
                    'endIndex': len(header) + 1
                },
                'textStyle': {
                    'bold': True,
                },
                'fields': 'bold'
            }
        }
    ]
    return requests


def create_header(header):
    requests = [
        {
            'insertText': {
                'location': {
                    'index': 1,
                },
                'text': header
            }
        },
        {
            'updateTextStyle': {
                'range': {
                    'startIndex': 1,
                    'endIndex': len(header) + 1
                },
                'textStyle': {
                    'weightedFontFamily': {
                        'fontFamily': 'Georgia'
                    },
                    'fontSize': {
                        'magnitude': 14,
                        'unit': 'PT'
                    },
                },
                'fields': 'weightedFontFamily, fontSize'
            }
        }
    ]
    return requests


def create_bold_sub_header(sub_header):
    sub_header = sub_header + ':'

    requests = [
        {
            'insertText': {
                'location': {
                    'index': 1,
                },
                'text': sub_header
            }
        },
        {
            'updateTextStyle': {
                'range': {
                    'startIndex': 1,
                    'endIndex': len(sub_header) + 1
                },
                'textStyle': {
                    'weightedFontFamily': {
                        'fontFamily': 'Georgia'
                    },
                    'fontSize': {
                        'magnitude': 11,
                        'unit': 'PT'
                    },
                },
                'fields': 'weightedFontFamily, fontSize'
            }
        },
        {
            'updateTextStyle': {
                'range': {
                    'startIndex': 1,
                    'endIndex': len(sub_header) + 1
                },
                'textStyle': {
                    'bold': True,
                },
                'fields': 'bold'
            }
        }
    ]
    return requests


def create_text_with_bullet_points(text):
    bullet_start_index = 1
    for char in text:
        if char != '\n':
            bullet_start_index = text.index(char)

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
                    'endIndex': len(text) + 1
                },
                'textStyle': {
                    'weightedFontFamily': {
                        'fontFamily': 'Georgia'
                    }
                },
                'fields': 'weightedFontFamily'
            }
        },
        {
            'createParagraphBullets': {
                'range': {
                    'startIndex': bullet_start_index,
                    'endIndex': len(text)
                },
                'bulletPreset': 'BULLET_DISC_CIRCLE_SQUARE'
            }
        }
    ]
    return requests
