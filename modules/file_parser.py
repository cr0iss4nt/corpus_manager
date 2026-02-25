from striprtf.striprtf import rtf_to_text
from pathlib import Path
import pdfplumber
import docx2txt  # add import for docx parsing

def parse_txt(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
        return content

def parse_rtf(filename):
    with open(filename) as f:
        content = f.read()
        text = rtf_to_text(content)
        return text

def parse_pdf(filename):
    text = ''
    with pdfplumber.open(filename) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + '\n'
    return text

def parse_docx(filename):
    text = docx2txt.process(filename)
    return text

def parse_file(filename):
    path = Path(filename)
    if path.suffix == '.rtf':
        return parse_rtf(filename)
    if path.suffix == '.txt':
        return parse_txt(filename)
    if path.suffix == '.pdf':
        return parse_pdf(filename)
    if path.suffix == '.docx':
        return parse_docx(filename)
    return ""