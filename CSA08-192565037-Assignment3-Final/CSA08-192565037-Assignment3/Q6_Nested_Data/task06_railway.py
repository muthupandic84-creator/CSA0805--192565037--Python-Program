"""Q6: Nested railway timetable and station index."""
import random
import time
from collections import defaultdict

TIMETABLE = {
    "12601": {"name": "Chennai Express", "stops": [
        ("Chennai", "06:00", "06:10"), ("Katpadi", "08:00", "08:05"), ("Bengaluru", "11:00", "11:10")],
        "days": {"Mon", "Wed", "Fri"}},
    "12602": {"name": "Bengaluru Mail", "stops": [
        ("Chennai", "07:00", "07:15"), ("Jolarpettai", "09:00", "09:05"), ("Bengaluru", "11:30", "11:40")],
        "days": {"Tue", "Thu", "Sat"}},
    "12603": {"name": "Coastal Express", "stops": [
        ("Chennai", "08:00", "08:10"), ("Vijayawada", "13:00", "13:05"), ("Visakhapatnam", "18:00", "18:10")],
        "days": {"Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"}},
    "12604": {"name": "Hill Passenger", "stops": [
        ("Salem", "05:30", "05:35"), ("Erode", "07:00", "07:05"), ("Coimbatore", "09:00", "09:10")],
        "days": {"Sun"}},
    "12605": {"name": "Southern Link", "stops": [
        ("Madurai", "06:30", "06:35"), ("Trichy", "09:00", "09:05"), ("Chennai", "14:00", "14:10")],
        "days": {"Mon", "Fri", "Sun"}},
}

def build_index(timetable):
    index = defaultdict(list)
    for train_no, info in timetable.items():
        for station, arrival, departure in info["stops"]:
            index[station].append((train_no, arrival, departure))
    return index

def query_scan(timetable, station, day):
    found = []
    for train_no, info in timetable.items():
        if day in info["days"]:
            for stop, arrival, departure in info["stops"]:
                if stop == station:
                    found.append((train_no, info["name"], arrival, departure))
    return sorted(found, key=lambda item: item[3])

def query_index(timetable, index, station, day):
    found = []
    for train_no, arrival, departure in index.get(station, []):
        info = timetable[train_no]
        if day in info["days"]:
            found.append((train_no, info["name"], arrival, departure))
    return sorted(found, key=lambda item: item[3])

def make_large_timetable(n):
    stations = ["Chennai", "Katpadi", "Salem", "Erode", "Madurai", "Trichy"]
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    data = {}
    for i in range(n):
        stops = [(s, "08:00", "08:05") for s in random.sample(stations, 3)]
        data[str(10000+i)] = {"name": f"Train {i}", "stops": stops, "days": set(random.sample(days, 4))}
    return data

def benchmark():
    print("trains,scan_seconds,indexed_seconds")
    for n in (100, 1_000, 10_000):
        data = make_large_timetable(n)
        start = time.perf_counter(); query_scan(data, "Chennai", "Mon"); scan_t = time.perf_counter()-start
        idx = build_index(data)
        start = time.perf_counter(); query_index(data, idx, "Chennai", "Mon"); index_t = time.perf_counter()-start
        print(f"{n},{scan_t:.6f},{index_t:.6f}")

if __name__ == "__main__":
    index = build_index(TIMETABLE)
    print("Chennai trains running Monday:", query_index(TIMETABLE, index, "Chennai", "Mon"))
    print("Unknown station:", query_index(TIMETABLE, index, "Unknown", "Mon"))
    print("Not-running day example:", query_index(TIMETABLE, index, "Chennai", "Tue"))
    for number, info in TIMETABLE.items():
        print(number, info["name"], "| days:", ", ".join(sorted(info["days"])))
        for stop in info["stops"]:
            print("   ", stop)
    benchmark()
