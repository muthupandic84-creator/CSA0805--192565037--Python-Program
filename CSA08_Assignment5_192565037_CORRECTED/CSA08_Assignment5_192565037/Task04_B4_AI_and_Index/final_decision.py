"""
Task B4 – Final engineering decision.
Implements the assignment's lexicon sentiment TODO, extractive summariser,
50-complaint comparison, parameterised chatbot and (station, day) index test.
"""
import csv
import re
import sqlite3
import time
from collections import Counter
from pathlib import Path

POSITIVE = {"good", "clean", "fast", "helpful", "improved"}
NEGATIVE = {"bad", "dirty", "slow", "rude", "smoke", "broken"}
NEGATORS = {"not", "never", "no"}
STOP_WORDS = {
    "the", "is", "a", "an", "and", "to", "of", "in", "was", "are",
    "for", "on", "it", "this", "that", "we", "our", "with", "from"
}

def score(text):
    """+1 per positive word, -1 per negative word; previous negator flips it."""
    words = text.lower().replace(".", " ").replace(",", " ").split()
    total = 0
    for index, word in enumerate(words):
        value = 1 if word in POSITIVE else -1 if word in NEGATIVE else 0
        if index > 0 and words[index - 1] in NEGATORS:
            value = -value
        total += value
    return total

def label(text):
    value = score(text)
    return "positive" if value > 0 else "negative" if value < 0 else "neutral"

def summarise(text, k=2):
    """Extract k sentences with the highest frequency of important words."""
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s.strip()]
    words = re.findall(r"[a-z]+", text.lower())
    frequencies = Counter(word for word in words if word not in STOP_WORDS)
    ranked = sorted(
        enumerate(sentences),
        key=lambda item: (
            -sum(frequencies[word] for word in re.findall(r"[a-z]+", item[1].lower())
                 if word not in STOP_WORDS),
            item[0]
        )
    )
    selected_indexes = {index for index, _ in ranked[:k]}
    return " ".join(sentence for index, sentence in enumerate(sentences)
                    if index in selected_indexes)

def first_k_sentences(text, k=2):
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s.strip()]
    return " ".join(sentences[:k])

def chatbot(question, con):
    match = re.search(
        r"pm\s*2?\.5\s+(?:level\s+)?in\s+([a-z ]+?)\s+today",
        question.lower()
    )
    if not match:
        return "Please ask: What is the PM2.5 in <station> today?"
    station = match.group(1).strip().title()
    row = con.execute(
        "SELECT AVG(pm25) FROM readings WHERE station=? AND day=?",
        (station, "2026-10-01")
    ).fetchone()
    if row is None or row[0] is None:
        return f"No reading found for {station}."
    return f"PM2.5 at {station}: {row[0]:.1f}"

# Fifty complaint examples with human-reviewed reference labels.
COMPLAINTS = [
("The roads are clean and buses are fast.", "positive"),
("Smoke from the factory makes the air bad.", "negative"),
("The staff were not helpful.", "negative"),
("Not bad, the service improved.", "positive"),
("The water is dirty near the market.", "negative"),
("The response team was helpful.", "positive"),
("Traffic is slow near the school.", "negative"),
("There is no smoke near my street.", "positive"),
("The officer was rude during my complaint.", "negative"),
("Air quality is good today.", "positive"),
("The road is broken and dirty.", "negative"),
("The buses are fast and clean.", "positive"),
("The air is not clean near the factory.", "negative"),
("The repair work improved the road.", "positive"),
("The service was not bad.", "positive"),
("The street is dirty but the staff were helpful.", "neutral"),
("Never good service from this office.", "negative"),
("No smoke was detected this morning.", "positive"),
("The bus was slow and the road was broken.", "negative"),
("The area is clean after the work.", "positive"),
("Great, another day of dirty air.", "negative"),
("The complaint desk was helpful but buses are slow.", "neutral"),
("The factory smoke is making the area dirty.", "negative"),
("The road is clean and the response was fast.", "positive"),
("The air is bad but the staff are helpful.", "neutral"),
("Not slow service, the team was fast.", "positive"),
("The water is not dirty now.", "positive"),
("The bus service is broken.", "negative"),
("The officer was not rude.", "positive"),
("The road condition is bad and traffic is slow.", "negative"),
("Clean streets and helpful workers.", "positive"),
("The smoke is not reduced.", "negative"),
("The service improved but the area is still dirty.", "neutral"),
("The bus was fast, but the road is broken.", "neutral"),
("No good response from the office.", "negative"),
("The new cleaning work is good.", "positive"),
("The factory is not producing smoke today.", "positive"),
("The staff were helpful and the process was fast.", "positive"),
("The road is bad, although the bus is fast.", "neutral"),
("The street is not clean and smells bad.", "negative"),
("The water is clean after repair.", "positive"),
("The response was slow and rude.", "negative"),
("The air quality is improved.", "positive"),
("Never dirty streets after the cleaning drive.", "positive"),
("The service is good but the waiting time is slow.", "neutral"),
("Smoke levels are high near the school.", "negative"),
("The road repair is not completed.", "neutral"),
("The team was not unhelpful.", "neutral"),
("The bus is fast and the station is clean.", "positive"),
("Bad air today, but helpful staff responded.", "neutral"),
]

def sentiment_experiment(folder):
    predicted = [label(text) for text, _ in COMPLAINTS]
    actual = [expected for _, expected in COMPLAINTS]
    agreement = sum(p == a for p, a in zip(predicted, actual))
    with open(folder/"complaints.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["complaint", "human_label", "predicted_label"])
        writer.writerows((text, actual_label, predicted_label)
                         for (text, actual_label), predicted_label
                         in zip(COMPLAINTS, predicted))
    print(f"Complaint count: {len(COMPLAINTS)}")
    print(f"Agreement with manual labels: {agreement}/{len(COMPLAINTS)} ({agreement/len(COMPLAINTS)*100:.1f}%)")
    example = ("The factory smoke is serious. Residents report dirty air. "
               "The council should inspect the factory. Smoke affects nearby schools.")
    print("Frequency-based summary:", summarise(example, 2))
    print("First-two-sentence summary:", first_k_sentences(example, 2))
    wrong = [(text, actual_label, predicted_label)
             for (text, actual_label), predicted_label
             in zip(COMPLAINTS, predicted) if actual_label != predicted_label]
    if wrong:
        print("Example scorer limitation:", wrong[0])
    else:
        print("Scorer limitation example:", "Great, another day of dirty air.",
              "Sarcasm is not understood from the word list alone.")

def index_experiment():
    con = sqlite3.connect(":memory:")
    con.execute("CREATE TABLE readings(station TEXT, day TEXT, pm25 REAL)")
    # 100 stations x 365 days x 6 readings = 219,000 rows.
    batch = []
    for station_no in range(1, 101):
        station = f"S{station_no:03d}"
        for day_no in range(365):
            day = f"2026-{day_no+1:03d}"
            for reading_no in range(6):
                batch.append((station, day, float((station_no*3 + day_no + reading_no) % 180)))
    con.executemany("INSERT INTO readings VALUES (?,?,?)", batch)
    con.commit()
    sql = "SELECT AVG(pm25) FROM readings WHERE station=? AND day=?"
    target = ("S087", "2026-200")
    # Repeat queries to reduce timer noise; use the same query before and after.
    start = time.perf_counter()
    for _ in range(300):
        con.execute(sql, target).fetchone()
    before = time.perf_counter() - start
    con.execute("CREATE INDEX idx_station_day ON readings(station, day)")
    con.commit()
    start = time.perf_counter()
    for _ in range(300):
        con.execute(sql, target).fetchone()
    after = time.perf_counter() - start
    print(f"Index experiment: rows={len(batch)}, 300 queries before={before:.6f}s, after={after:.6f}s")
    print("Query plan after index:")
    for row in con.execute("EXPLAIN QUERY PLAN " + sql, target):
        print(" ", row[-1])
    con.close()

def main():
    folder = Path(__file__).parent
    sentiment_experiment(folder)
    con = sqlite3.connect(":memory:")
    con.execute("CREATE TABLE readings(station TEXT, day TEXT, pm25 REAL)")
    con.executemany(
        "INSERT INTO readings VALUES (?,?,?)",
        [("Adyar","2026-10-01",48.0), ("Adyar","2026-10-01",52.0),
         ("Guindy","2026-10-01",95.0)]
    )
    print("CHATBOT:", chatbot("What is the PM2.5 in Adyar today?", con))
    con.close()
    index_experiment()
    print("Decision: retain validated readings in an indexed relational database; batch-process station files; "
          "use a reviewed, locally trained sentiment model when complaint volume and language variation exceed "
          "the lexicon's capability. Keep human review for ambiguous or high-impact complaints.")

if __name__ == "__main__":
    main()
