from striprtf.striprtf import rtf_to_text
from pathlib import Path


def parse_txt(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
        return content

def parse_rtf(filename):
    with open(filename) as f:
        content = f.read()
        text = rtf_to_text(content)
        return text

def parse_file(filename):
    path = Path(filename)
    if path.suffix == '.rtf':
        return parse_rtf(filename)
    if path.suffix == '.txt':
        return parse_txt(filename)
