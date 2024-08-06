from common.defs import UI_ELEMENTS
from elements.title import Title

"""Content always needs to be a string so we handle that conversion here"""
def format_content(content, width, height, b_size, content_height=0, offset=0)->str:
    if isinstance(content, UI_ELEMENTS):
        content.width = width
        if isinstance(content, Title):
            for element in content.content:
                if element.get('ascii'):
                    content_height += len(element['ascii'][0])
                else:
                    content_height += len(element['string'])
            offset += (((height - (b_size*2))-content_height) // 2)
        content = content.render()
    elif isinstance(content, list):
        content = "\n".join(content)
    elif isinstance(content, dict):
        content = content.__repr__()
    elif isinstance(content, int):
        content = content.__str__()
    return content, offset

