import time


def analyze_pos_frequency(words):
    t1 = time.time()
    parts_of_speech = set(word[4] for word in words)
    frequency = {pos:0 for pos in parts_of_speech}
    for word in words:
        frequency[word[4]] += word[2]
    result = [(k,v) for k, v in sorted(frequency.items(), key=lambda item: item[1], reverse=True)]
    dt = time.time() - t1
    print(f"Fetched POS frequency in {dt:.3f} seconds")
    return result