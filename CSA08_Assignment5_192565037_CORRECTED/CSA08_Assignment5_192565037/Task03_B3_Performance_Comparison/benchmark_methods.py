"""
Task B3 – Compare Python loops, pandas groupby and SQL GROUP BY.
Generates one year of hourly readings: 8,760 rows per station.
"""
import csv
import io
import sqlite3
import time
import cProfile
import pstats
from pathlib import Path
from datetime import date, timedelta
from collections import defaultdict
import statistics

try:
    import pandas as pd
except ImportError:
    pd = None

def generate_dataset(path, station_count):
    start = date(2026, 1, 1)
    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["station", "day", "hour", "pm25"])
        for station_no in range(1, station_count + 1):
            station = f"S{station_no:03d}"
            for hour_index in range(365 * 24):
                day = start + timedelta(days=hour_index // 24)
                hour = hour_index % 24
                pm25 = round(12 + ((station_no * 7 + hour * 3 + day.day) % 140), 2)
                writer.writerow([station, day.isoformat(), f"{hour:02d}:00", pm25])

def python_csv_groupby(csv_path):
    """Plain csv-module solution: keep each group's values and call statistics.mean."""
    grouped = defaultdict(list)
    with open(csv_path, newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            key = (row["station"], row["day"])
            grouped[key].append(float(row["pm25"]))
    return {key: round(statistics.mean(values), 6)
            for key, values in grouped.items()}

def pandas_groupby(csv_path):
    if pd is None:
        raise RuntimeError("pandas is not installed. Run: python -m pip install pandas")
    frame = pd.read_csv(csv_path)
    grouped = frame.groupby(["station", "day"], sort=True)["pm25"].mean()
    return {key: round(float(value), 6) for key, value in grouped.items()}

def sql_groupby(csv_path, database_path):
    con = sqlite3.connect(database_path)
    con.execute("DROP TABLE IF EXISTS readings")
    con.execute("""CREATE TABLE readings(
        station TEXT NOT NULL, day TEXT NOT NULL,
        hour TEXT NOT NULL, pm25 REAL NOT NULL)""")
    with open(csv_path, newline="", encoding="utf-8") as file:
        rows = ((r["station"], r["day"], r["hour"], float(r["pm25"]))
                for r in csv.DictReader(file))
        con.executemany("INSERT INTO readings VALUES (?,?,?,?)", rows)
    con.commit()
    result = {(station, day): round(mean, 6)
              for station, day, mean in con.execute(
                  "SELECT station, day, AVG(pm25) FROM readings GROUP BY station, day")}
    con.close()
    return result

def timed(function, *args):
    start = time.perf_counter()
    result = function(*args)
    return result, time.perf_counter() - start

def main():
    folder = Path(__file__).parent
    timing_rows = []
    for station_count in (1, 12, 120):
        csv_path = folder / f"readings_{station_count}_stations.csv"
        db_path = folder / f"readings_{station_count}_stations.sqlite"
        generate_dataset(csv_path, station_count)

        python_result, python_seconds = timed(python_csv_groupby, csv_path)
        sql_result, sql_seconds = timed(sql_groupby, csv_path, db_path)
        assert python_result == sql_result, "Python CSV and SQL daily means do not match"

        timing_rows.append((station_count, "Python csv loops", len(python_result), python_seconds))
        timing_rows.append((station_count, "SQL GROUP BY", len(sql_result), sql_seconds))

        if pd is not None:
            pandas_result, pandas_seconds = timed(pandas_groupby, csv_path)
            assert python_result == pandas_result, "Python and pandas daily means do not match"
            timing_rows.append((station_count, "pandas groupby", len(pandas_result), pandas_seconds))
            print(f"{station_count} stations: {len(python_result)} daily means; all three methods agree")
        else:
            print(f"{station_count} stations: Python and SQL agree; pandas unavailable")

    print("\\nTIMING RESULTS (station count, method, groups, seconds)")
    for row in timing_rows:
        print(f"{row[0]:3} | {row[1]:18} | {row[2]:6} | {row[3]:.6f}")

    # Profile the plain Python implementation on the 12-station data.
    profile = cProfile.Profile()
    profile.enable()
    python_csv_groupby(folder/"readings_12_stations.csv")
    profile.disable()
    stream = io.StringIO()
    pstats.Stats(profile, stream=stream).sort_stats("cumulative").print_stats(12)
    (folder/"cprofile.txt").write_text(stream.getvalue(), encoding="utf-8")
    with open(folder/"timings.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["stations", "method", "daily_groups", "seconds"])
        writer.writerows(timing_rows)
    print("\\nProfile saved: cprofile.txt")
    print("Timing table saved: timings.csv")
    print("For a quick one-time analysis, Python/pandas is convenient; for a daily automated report, store readings in SQL and use indexed GROUP BY queries.")

if __name__ == "__main__":
    main()
