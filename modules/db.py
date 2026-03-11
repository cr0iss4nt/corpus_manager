import sqlite3

import pymorphy3

from modules import file_parser, lexemizer

import time

from modules.directory_file_finder import get_files_in_directory

DATABASE_NAME = 'corpus.db'
BOOKS_FOLDER = 'books/'
CONTEXT_SIZE = 7
PAGE_LIMIT = 100

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

    cursor.execute('''
    CREATE INDEX IF NOT EXISTS idx_concordance
    ON Corpus(id)
    ''')

    cursor.execute('''
    CREATE INDEX IF NOT EXISTS idx_concordance
    ON Corpus(id)
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

import sqlite3
import time

def get_words(query=''):
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

    dt = time.time() - t1
    print(f"Fetched words (query='{query}') in {dt:.3f} seconds")

    word_number = sum([int(i[2]) for i in words if query in i[1]])
    lemma_number = sum([int(i[2]) for i in words if query in i[3]])
    result_number = sum([int(i[2]) for i in words if query in i[1] or query in i[3]])

    total_pages = (len(words) + PAGE_LIMIT - 1) // PAGE_LIMIT

    return words, word_number, lemma_number, result_number, total_pages

def get_word_features(words):
    t1 = time.time()

    word_features = sorted(list(set([(i[1], i[3], i[4], i[5]) for i in words])))
    dt = time.time() - t1
    print(f"Fetched word features in {dt:.3f} seconds")

    return word_features

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
        print(f"Added word ({book}): {word}")
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
    clean_filename = filename.split('/')[-1]
    t1 = time.time()
    for lexeme in lexemes:
        if lexeme[0].isnumeric():
            add_word(word=lexeme[0], lemma=lexeme[0], part_of_speech='ЧИСЛ',
                     features='', book=clean_filename, connection=connection)
        else:
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
                     features=features, book=clean_filename, connection=connection)
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
Количество: {word[2]}
Лемма: {word[3]}
Часть речи: {word[4]}
Характеристики: {word[5]}
Источник: {word[6]}""")
    return '\n\n\n'.join(output)


def get_concordance(query, book):
    connection = sqlite3.connect('corpus.db')
    cursor = connection.cursor()

    t1 = time.time()

    cursor.execute("""
                    SELECT DISTINCT id
                    FROM Corpus
                    WHERE word = ? AND book = ?
                    """, (query,book))
    ids = [int(i[0]) for i in cursor.fetchall()]

    concordance = []
    for word_id in ids:
        cursor.execute("""
                    SELECT DISTINCT word
                    FROM Corpus
                    WHERE id BETWEEN ? AND ?
                    """, (word_id - CONTEXT_SIZE, word_id + CONTEXT_SIZE))
        context = cursor.fetchall()
        concordance.append(f"...{' '.join([i[0].upper() if i[0]==query else i[0] for i in context])}...",)

    connection.close()

    dt = time.time() - t1
    print(f"Got concordance (query='{query}') in {dt:.3f} seconds")

    return concordance

def get_abnormal_words():
    init_db()

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    t1 = time.time()

    cursor.execute("""
            SELECT id, word, COUNT(*) as word_count, lemma, part_of_speech, features, book
            FROM Corpus
            WHERE part_of_speech=?
            GROUP BY word, book
            ORDER BY word_count DESC, word, book
            """, ('',))
    words = cursor.fetchall()

    connection.close()

    dt = time.time() - t1
    print(f"Fetched abnormal words in {dt:.3f} seconds")

    return words