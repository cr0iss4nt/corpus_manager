import pymorphy3

def get_part_of_speech(word, morph: pymorphy3.MorphAnalyzer()):
    parsed_word = morph.parse(word)[0]
    return parsed_word.tag.POS

#def inflect(word, morph: pymorphy3.MorphAnalyzer(), word_features: set):
#    parsed_word = morph.parse(word)[0]
#    word_features = word_features - {'NONE'}
#    inflected_word = parsed_word.inflect(word_features)
#    return inflected_word[0] if inflected_word is not None else 'Такой формы не существует!'