from clients.fetch_note_json import fetch_note_json


def process_text_nodes(children: list) -> str:
    """
    Process and combine adjacent text nodes, applying formatting where necessary.
    """
    combined_text = []
    current_text = ""

    for child in children:
        if child['type'] == 'text':
            # If the text should be bold
            if child.get('format') == 1:
                # If there's existing non-bold text, append it first
                if current_text:
                    combined_text.append(current_text)
                    current_text = ""
                combined_text.append(f"**{child['text']}**")
            else:
                # Combine adjacent non-bold text nodes
                current_text += child['text']
        else:
            # If there's existing non-bold text, append it first
            if current_text:
                combined_text.append(current_text)
                current_text = ""
            combined_text.append(json_to_md(child))

    # Append any remaining text
    if current_text:
        combined_text.append(current_text)

    return ''.join(combined_text)


def json_to_md(node: dict, parent_list_type: str = None) -> str:
    """
    Convert a Genei note JSON node to Markdown.
    """
    node_type = node['type']

    if node_type in ['text', 'code-highlight']:
        node_text = node.get('text')
        if node_text and node_text != '[link]':
            return f"**{node_text}**" if node.get('format') == '1' else node_text

    if node_type == 'heading':
        level = int(node['tag'][1])
        return f"{'#' * level} " + ' '.join([json_to_md(child) for child in node['children']]) + "\n"

    if node_type == 'list':
        list_type = node.get('listType', 'bullet')
        return '\n'.join([json_to_md(child, list_type) for child in node['children']])

    if node_type == 'listitem':
        if parent_list_type == 'bullet':
            prefix = "- "
        else:
            prefix = f"{node['value']}. "
        indent = node.get('indent', 0)
        prefix = '\t' * indent + prefix

        combined_text = process_text_nodes(node['children'])
        if node['children'] and node['children'][0].get('type') == 'list':
            return combined_text
        else:
            return prefix + combined_text

    if node_type == 'code':
        return f"```{node.get('language', '')}\n" + ''.join([json_to_md(child) for child in node['children']]) + "\n```"

    if node_type == 'equation':
        sign = '$' if node.get('inline', False) else '$$'
        return sign + node.get('equation', '') + sign

    if node_type == 'quote':
        return '\n> ' + ' '.join([json_to_md(child) for child in node['children']]) + "\n"

    if node_type == 'resource-link':
        return ' '.join([json_to_md(child) for child in node['children']])

    if node_type in ['paragraph', 'root']:
        return '\n'.join([json_to_md(child) for child in node['children']])

    if node_type == 'linebreak':
        return '\n'

    return ''


if __name__ == '__main__':
    note_name = "1.0 - Quantitative Data Analysis - 'Introduction' - Week 1 Lecture Notes"
    note_json = fetch_note_json(note_name)
    assert note_json, f'No note found with the name: {note_name}'
    markdown_output = json_to_md(note_json)
    assert markdown_output, 'Conversion resulted in empty markdown output'
    print(markdown_output)
