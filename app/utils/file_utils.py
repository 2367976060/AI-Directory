import re


def sanitize_filename(name):
    name = re.sub(r'[<>:"/\\|?*]', '_', name)
    name = name.strip('. ')
    if not name:
        name = 'unnamed'
    return name


def ensure_utf8(content):
    if isinstance(content, str):
        return content.encode('utf-8').decode('utf-8')
    return content
