"""
Task B1 – Implement and validate the cleaning pipeline.
The first two functions complete the exact TODO program from the assignment.
The remaining functions demonstrate cleaning, SQLite storage and visualisation.
"""
import csv
import io
import sqlite3
import statistics
from pathlib import Path
from datetime import datetime

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None

# Original assignment sample, extended with a >999 sensor-fault test row.
RAW = """station,date,pm25
Adyar,2026-10-01,48
Adyar,2026-10-02,NA
Adyar,2026-10-03,
Guindy,2026-10-01,95
Guindy,2026-10-02,-5
Guindy,2026-10-03,121
Velachery,2026-10-01,1001
"""

def load_clean(text):
    """Return (station, date, pm25) tuples for valid non-negative readings."""
    rows = []
    reader = csv.DictReader(io.StringIO(text))
    required = {"station", "date", "pm25"}
    if not reader.fieldnames or not required.issubset(reader.fieldnames):
        raise ValueError("CSV must contain station, date and pm25 columns")
    for row in reader:
        raw_value = (row.get("pm25") or "").strip()
        if raw_value.upper() in ("", "NA"):
            continue
        try:
            pm25 = float(raw_value)
        except ValueError:
            continue
        if pm25 < 0 or pm25 > 999:
            continue
        station = (row.get("station") or "").strip()
        day = (row.get("date") or "").strip()
        if not station or not day:
            continue
        # Validate the required ISO date format.
        datetime.strptime(day, "%Y-%m-%d")
        rows.append((station, day, pm25))
    return rows

def min_max(values):
    """Scale values to 0–1 and round to three decimals."""
    values = list(values)
    if not values:
        return []
    low, high = min(values), max(values)
    if high == low:
        return [0.0 for _ in values]
    return [round((value - low) / (high - low), 3) for value in values]

def demonstrate_exact_todo():
    cleaned = load_clean(RAW)
    print("TODO 1 OUTPUT:", cleaned)
    print("TODO 2 OUTPUT:", min_max([pm for _, _, pm in cleaned]))
    return cleaned

# A richer B1 validation file exercises missing values, invalid values,
# duplicates, Fahrenheit conversion, malformed date and station formatting.
FULL_RAW = """station,date,hour,pm25,pm10,no2,temperature,unit
Adyar,2026-10-01,08:00,48,80,22,30,C
Adyar,2026-10-02,08:00,NA,75,20,31,C
Adyar,2026-10-03,08:00,,70,19,32,C
Adyar,2026-10-01,08:00,48,80,22,30,C
Guindy,2026-10-01,08:00,95,130,35,86,F
Guindy,2026-10-02,08:00,-5,120,31,87,F
Guindy,2026-10-03,08:00,121,150,40,88,F
Velachery,2026-10-01,08:00,1001,140,42,33,C
Velachery,2026-10-02,08:00,65,110,30,34,C
"""

def clean_full_csv(text):
    reader = csv.DictReader(io.StringIO(text))
    required = {"station","date","hour","pm25","pm10","no2","temperature","unit"}
    if not reader.fieldnames or not required.issubset(reader.fieldnames):
        raise ValueError("CSV is missing one or more required columns")
    output, seen = [], set()
    for row in reader:
        station = row["station"].strip().title()
        day = datetime.strptime(row["date"].strip(), "%Y-%m-%d").date().isoformat()
        hour = row["hour"].strip()
        raw = (row["pm25"] or "").strip()
        if raw.upper() in ("", "NA"):
            continue
        try:
            pm25 = float(raw)
            pm10 = float(row["pm10"])
            no2 = float(row["no2"])
            temp = float(row["temperature"])
        except (TypeError, ValueError):
            continue
        if pm25 < 0 or pm25 > 999 or pm10 < 0 or no2 < 0:
            continue
        key = (station, day, hour)
        if key in seen:
            continue
        seen.add(key)
        if row["unit"].strip().upper() == "F":
            temp = (temp - 32) * 5 / 9
        output.append((station, day, hour, pm25, pm10, no2, round(temp, 2)))
    return output

def store_and_query(rows, db_path):
    if db_path.exists():
        db_path.unlink()
    con = sqlite3.connect(db_path)
    con.execute("""CREATE TABLE readings(
        station TEXT NOT NULL, day TEXT NOT NULL, hour TEXT NOT NULL,
        pm25 REAL, pm10 REAL, no2 REAL, temperature_c REAL,
        PRIMARY KEY(station, day, hour))""")
    con.executemany("INSERT INTO readings VALUES (?,?,?,?,?,?,?)", rows)
    con.commit()
    queries = {
        "Adyar October average PM2.5":
            ("SELECT AVG(pm25) FROM readings WHERE station=? AND day BETWEEN ? AND ?",
             ("Adyar","2026-10-01","2026-10-31")),
        "Maximum PM10 by station":
            ("SELECT station, MAX(pm10) FROM readings GROUP BY station ORDER BY station", ()),
        "Daily mean PM2.5 by station":
            ("SELECT station, day, ROUND(AVG(pm25),2) FROM readings GROUP BY station, day ORDER BY station, day", ())
    }
    for title, (sql, params) in queries.items():
        print(title + ":")
        for result in con.execute(sql, params):
            print(" ", result)
    con.close()

def create_charts(rows, output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    # Chart data
    by_day, by_station, by_hour = {}, {}, {}
    for row in rows:
        station, day, hour, pm25, pm10, no2, temp = row
        by_day.setdefault(day, []).append(pm25)
        by_station.setdefault(station, []).append(pm25)
        by_hour.setdefault(hour[:2], []).append(pm25)
    if plt is None:
        # A dependency-free chart fallback: write SVG charts.
        def svg_bar(path, title, labels, vals):
            width, height = 760, 380
            maxv = max(vals) if vals else 1
            bars = []
            for i,(lab,val) in enumerate(zip(labels, vals)):
                x=80+i*max(1,600//max(1,len(vals))); h=230*val/maxv
                bars.append(f'<rect x="{x}" y="{290-h}" width="28" height="{h}" fill="white" stroke="black"/>'
                            f'<text x="{x}" y="315" font-size="10">{lab}</text>')
            path.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}"><text x="20" y="25">{title}</text>'+''.join(bars)+'</svg>',encoding="utf-8")
        svg_bar(output_dir/"daily_pm25_trend.svg","Daily PM2.5 trend",list(sorted(by_day)),[statistics.mean(by_day[k]) for k in sorted(by_day)])
        svg_bar(output_dir/"station_comparison.svg","Station comparison",list(by_station),[statistics.mean(v) for v in by_station.values()])
        svg_bar(output_dir/"temperature_vs_pm25.svg","Temperature and PM2.5",list(range(len(rows))),[r[3] for r in rows])
        svg_bar(output_dir/"worst_hours.svg","PM2.5 by hour",list(by_hour),[statistics.mean(v) for v in by_hour.values()])
        return
    days=sorted(by_day)
    plt.figure(); plt.plot(days,[statistics.mean(by_day[d]) for d in days],marker="o")
    plt.xlabel("Date"); plt.ylabel("Mean PM2.5"); plt.title("PM2.5 Trend Over Time"); plt.xticks(rotation=35); plt.tight_layout()
    plt.savefig(output_dir/"daily_pm25_trend.png"); plt.close()
    plt.figure(); plt.bar(list(by_station),[statistics.mean(v) for v in by_station.values()])
    plt.xlabel("Station"); plt.ylabel("Mean PM2.5"); plt.title("Comparison of Stations"); plt.tight_layout()
    plt.savefig(output_dir/"station_comparison.png"); plt.close()
    plt.figure(); plt.scatter([r[6] for r in rows],[r[3] for r in rows])
    plt.xlabel("Temperature (C)"); plt.ylabel("PM2.5"); plt.title("Temperature vs PM2.5"); plt.tight_layout()
    plt.savefig(output_dir/"temperature_vs_pm25.png"); plt.close()
    plt.figure(); plt.bar(list(by_hour),[statistics.mean(v) for v in by_hour.values()])
    plt.xlabel("Hour"); plt.ylabel("Mean PM2.5"); plt.title("Hours with the Worst Air"); plt.tight_layout()
    plt.savefig(output_dir/"worst_hours.png"); plt.close()

def main():
    folder = Path(__file__).parent
    print("BEFORE CLEANING: rows =", len(FULL_RAW.strip().splitlines()) - 1)
    clean = demonstrate_exact_todo()
    full = clean_full_csv(FULL_RAW)
    print("AFTER CLEANING:", full)
    print("AFTER CLEANING ROW COUNT:", len(full))
    store_and_query(full, folder/"air_quality.sqlite")
    create_charts(full, folder/"charts")
    print("Charts saved in:", folder/"charts")

if __name__ == "__main__":
    main()
