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
    features TEXT,
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
        SELECT id, word, COUNT(*) as word_count, lemma, part_of_speech, features, book
        FROM Corpus
        WHERE word LIKE ? OR lemma LIKE ?
        GROUP BY word, book
        ORDER BY word_count DESC, word, book
        """, ('%' + query + '%', '%' + query + '%'))
    words = cursor.fetchall()

    connection.close()

    dt = time.time()-t1
    print(f"Fetched words (query='{query}') in {dt:.3f} seconds")

    word_number = sum([int(i[2]) for i in words if query in i[1]])
    lemma_number = sum([int(i[2]) for i in words if query in i[3]])
    result_number = sum([int(i[2]) for i in words if query in i[1] or query in i[3]])

    return words, word_number, lemma_number, result_number

def get_word_features(query = ''):
    init_db()

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    t1 = time.time()

    cursor.execute("""
            SELECT DISTINCT word, lemma, part_of_speech, features
            FROM Corpus
            WHERE word LIKE ? OR lemma LIKE ?
            ORDER BY word
            """, ('%' + query + '%', '%' + query + '%'))
    words = cursor.fetchall()

    connection.close()

    dt = time.time() - t1
    print(f"Fetched word features (query='{query}') in {dt:.3f} seconds")

    return words

def add_word(word, lemma, part_of_speech, features, book, connection=None):
    has_outer_connection = True
    if connection is None:
        has_outer_connection = False
        connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    try:
        cursor.execute('''
        INSERT INTO Corpus(word, lemma, part_of_speech, features, book)
        VALUES
        (?, ?, ?, ?, ?)
        ''', (word, lemma, part_of_speech, features, book))
        print(f"Added word: {word}")
    except Exception as e:
        print(f"Error adding word: {word}\nError: {e}")

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
        tag = morph.parse(lexeme[0])[0].tag

        try:
            part_of_speech = morph.lat2cyr(tag.POS)
        except:
            part_of_speech = ""
        try:
            features = morph.lat2cyr(tag).split(' ')[1]
        except:
            features = ""

        add_word(word=lexeme[0], lemma=lexeme[1], part_of_speech=part_of_speech,
                 features=features, book=filename, connection=connection)
    dt = time.time()-t1
    if not has_outer_connection:
        connection.commit()
        connection.close()
    print(f"Added words from {filename} in {dt:.3f} seconds")

def build_corpus(morph: pymorphy3.MorphAnalyzer(), directory=BOOKS_FOLDER):
    clear_db()
    filenames = get_files_in_directory(directory)
    connection = sqlite3.connect(DATABASE_NAME)
    t1 = time.time()
    for filename in filenames:
        add_words_from_file(filename, morph, connection=connection)
    connection.commit()
    connection.close()
    dt = time.time() - t1
    print(f"Corpus built from {directory} in {dt:.3f} seconds")

def db_to_text(words):
    output = []
    for word in words:
        output.append(f"""{word[1].upper()}
Лемма: {word[2]}
Часть речи: {word[3]}
Характеристики: {word[4]}
Источник: {word[5]}""")
    return '\n\n\n'.join(output)