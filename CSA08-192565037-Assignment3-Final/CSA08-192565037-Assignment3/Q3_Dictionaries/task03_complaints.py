"""Q3: Complaint word frequency, district grouping and performance."""
import random
import re
import time
from collections import Counter

STOP = {"not", "high", "the", "is", "a", "and", "to", "of"}

def frequencies(texts, stop):
    counts = {}
    for text in texts:
        words = re.findall(r"[a-z]+", text.lower())
        for word in words:
            if word not in stop:
                counts[word] = counts.get(word, 0) + 1
    return counts

def top(counts, k):
    return sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:k]

def group_by_district(records):
    grouped = {}
    for district, crop, complaint in records:
        grouped.setdefault(district, []).append((crop, complaint))
    return grouped

def list_count_method(texts, stop):
    words = []
    for text in texts:
        words.extend(w for w in re.findall(r"[a-z]+", text.lower()) if w not in stop)
    return {word: words.count(word) for word in set(words)}

def benchmark():
    random.seed(42)
    vocabulary = ["seed", "price", "fertiliser", "water", "crop", "pest", "subsidy"]
    print("complaints,dictionary_seconds,list_count_seconds,counter_seconds")
    for n in (1_000, 10_000, 100_000):
        texts = [" ".join(random.choices(vocabulary, k=8)) for _ in range(n)]
        start = time.perf_counter(); d = frequencies(texts, STOP); td = time.perf_counter()-start
        start = time.perf_counter(); l = list_count_method(texts, STOP); tl = time.perf_counter()-start
        start = time.perf_counter(); c = Counter(w for t in texts for w in re.findall(r"[a-z]+", t.lower()) if w not in STOP); tc = time.perf_counter()-start
        assert d == l == dict(c)
        print(f"{n},{td:.6f},{tl:.6f},{tc:.6f}")

if __name__ == "__main__":
    calls = [
        "seeds not received seeds delayed",
        "fertiliser price high",
        "seeds price high subsidy not received",
    ]
    print(top(frequencies(calls, {"not", "high"}), 3))
    records = [
        ("Madurai", "rice", "Seeds not received"),
        ("Salem", "cotton", "Pest attack reported"),
        ("Madurai", "rice", "Water supply delayed"),
    ]
    print("District groups:", group_by_district(records))
    print("Empty text:", frequencies([""], STOP))
    print("Case/punctuation:", frequencies(["SEEDS, seeds! Price."], STOP))
    benchmark()
