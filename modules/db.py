import sqlite3

import pymorphy3

from modules import file_parser, lexemizer

import time

from modules.directory_file_finder import get_files_in_directory

DATABASE_NAME = 'corpus.db'
BOOKS_FOLDER = 'books/'

def init_db():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Corpus (
    id INTEGER PRIMARY KEY,
    word TEXT NOT NULL,
    lemma TEXT NOT NULL,
    part_of_speech TEXT,
    book TEXT NOT NULL
    )
    ''')

    connection.commit()
    connection.close()

def clear_db():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("DELETE FROM Corpus")

    connection.commit()
    connection.close()

    print("Database cleared")

def get_words(query = ''):
    init_db()

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    t1 = time.time()

    cursor.execute("""
        SELECT DISTINCT * FROM
        Corpus
        WHERE word LIKE ? OR lemma LIKE ?
        ORDER BY id
        """, ('%' + query + '%', '%' + query + '%'))
    words = cursor.fetchall()

    connection.close()

    dt = time.time()-t1
    print(f"Fetched words (query='{query}') in {dt} seconds")

    word_number = len([i for i in words if query.lower() in i[1].lower()])
    lemma_number = len([i for i in words if query.lower() in i[2].lower()])

    return words, word_number, lemma_number

def add_word(word, lemma, part_of_speech, book, connection=None):
    has_outer_connection = True
    if connection is None:
        has_outer_connection = False
        connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    try:
        cursor.execute('''
        INSERT INTO Corpus(word, lemma, part_of_speech, book)
        VALUES
        (?, ?, ?, ?)
        ''', (word, lemma, part_of_speech, book))
        print(f"Added word: {word}")
    except:
        print(f"Error adding word: {word}")

    if not has_outer_connection:
        connection.commit()
        connection.close()

def add_words_from_file(filename, morph: pymorphy3.MorphAnalyzer(), connection=None):
    text = file_parser.parse_file(filename)
    lexemes = lexemizer.text_to_lexemes(text, morph)

    has_outer_connection = True
    if connection is None:
        has_outer_connection = False
        connection = sqlite3.connect(DATABASE_NAME)
    t1 = time.time()
    for lexeme in lexemes:
        part_of_speech = morph.parse(lexeme[0])[0].tag.POS
        add_word(word=lexeme[0], lemma=lexeme[1], part_of_speech=part_of_speech,
                 book=filename, connection=connection)
    dt = time.time()-t1
    if not has_outer_connection:
        connection.commit()
        connection.close()
    print(f"Added words from {filename} in {dt} seconds")

def build_corpus(morph: pymorphy3.MorphAnalyzer(), directory=BOOKS_FOLDER):
    filenames = get_files_in_directory(directory)
    connection = sqlite3.connect(DATABASE_NAME)
    t1 = time.time()
    for filename in filenames:
        add_words_from_file(filename, morph, connection=connection)
    connection.commit()
    connection.close()
    dt = time.time() - t1
    print(f"Corpus built from {directory} in {dt} seconds")


# change the base and the ending of the word
#def edit_word(word, base, ending):
#    connection = sqlite3.connect(DATABASE_NAME)
#    cursor = connection.cursor()
#
#    cursor.execute('''
#    UPDATE Dictionary
#    SET base=?, ending=?
#    WHERE word=?
#    ''', (base, ending, word))
#
#   connection.commit()
#   connection.close()


#def delete_word(word):
#    connection = sqlite3.connect(DATABASE_NAME)
#    cursor = connection.cursor()
#
#    cursor.execute('''
#    DELETE FROM Dictionary
#    WHERE word=?
#    ''', (word,))
#
#    connection.commit()
#    connection.close()

def db_to_text(words):
    output = []
    for word in words:
        output.append(f"""{word[1].upper()}
Лемма: {word[2]}
Часть речи: {word[3]}
Источник: {word[4]}""")
    return '\n\n\n'.join(output)