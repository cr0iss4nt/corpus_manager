from itertools import islice

def analyze_pos_frequency(words):
    parts_of_speech = set(word[3] for word in words)
    frequency = {pos:0 for pos in parts_of_speech}
    for word in words:
        frequency[word[3]] += 1
    result = {k: v for k, v in sorted(frequency.items(), key=lambda item: item[1], reverse=True)}
    return result


def split_dict(d):
    items = iter(d.items())
    first_half = dict(islice(items, (len(d)+1)//2))
    second_half = dict(items)
    return first_half, second_half
