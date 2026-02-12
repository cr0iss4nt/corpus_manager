from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pymorphy3

import time

RUSSIAN_LETTERS = set('ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДДЖЭЯЧСМИТЬБЮЁйцукенгшщзхъфывапролджэячсмитьбюё')


def is_russian_text(text):
    return not set(text) - RUSSIAN_LETTERS

def tokenize_text(text):
    tokens = word_tokenize(text)
    filtered_tokens = [word for word in tokens if is_russian_text(word)]
    return filtered_tokens

def tokens_to_lexemes(tokens, morph: pymorphy3.MorphAnalyzer()):
    lexemes = []
    for token in tokens:
        p = morph.parse(token)[0]
        lexemes.append((token, p.normal_form))
    return lexemes

def text_to_lexemes(text, morph: pymorphy3.MorphAnalyzer()):
    t1 = time.time()
    tokens = tokenize_text(text)
    lexemes = tokens_to_lexemes(tokens, morph)
    dt = time.time()-t1
    print(f"Text lexemized in {dt} seconds")
    return lexemes

