import sqlite3
import time
from itertools import islice

from modules.db import DATABASE_NAME


#def analyze_pos_frequency(words):
#    parts_of_speech = set(word[4] for word in words)
#    frequency = {pos:0 for pos in parts_of_speech}
#    for word in words:
#        frequency[word[4]] += word[2]
#    result = {k: v for k, v in sorted(frequency.items(), key=lambda item: item[1], reverse=True)}
#    return result

def analyze_pos_frequency(query=''):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    t1 = time.time()

    cursor.execute("""
            SELECT part_of_speech, SUM(word_count) AS total_count
            FROM (
                SELECT part_of_speech, COUNT(*) AS word_count
                FROM Corpus
                WHERE word LIKE ? OR lemma LIKE ?
                GROUP BY part_of_speech
            )
            GROUP BY part_of_speech
            ORDER BY total_count DESC, part_of_speech
            """, ('%' + query + '%', '%' + query + '%'))
    pos_frequency = cursor.fetchall()

    connection.close()

    dt = time.time() - t1
    print(f"Fetched POS frequency (query='{query}') in {dt:.3f} seconds")

    return pos_frequency


#def split_dict(d):
#    items = iter(d.items())
#    first_half = dict(islice(items, (len(d)+1)//2))
#    second_half = dict(items)
#    return first_half, second_half
