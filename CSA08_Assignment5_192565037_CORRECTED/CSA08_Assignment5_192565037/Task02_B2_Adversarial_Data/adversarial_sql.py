import sqlite3, csv, io
from pathlib import Path

def validate_csv(text):
    if not text.strip(): return "ERROR: empty file"
    reader = csv.DictReader(io.StringIO(text))
    required = {"station","date","pm25"}
    if not required.issubset(reader.fieldnames or []):
        return "ERROR: missing required column(s)"
    return f"OK: {sum(1 for _ in reader)} data row(s)"

def main():
    print("MISSING COLUMN:", validate_csv("station,date\\nAdyar,2026-10-01"))
    print("WRONG DELIMITER:", validate_csv("station;date;pm25\\nAdyar;2026-10-01;48"))
    # UTF-16 bytes decoded as UTF-8 deliberately simulate an encoding mismatch.
    encoded_as_utf16 = "சென்னை,2026-10-01,48".encode("utf-16")
    try:
        encoded_as_utf16.decode("utf-8")
        print("ENCODING: unexpectedly decoded")
    except UnicodeError:
        print("ENCODING: ERROR - UTF-16 data cannot be decoded as UTF-8")
    print("EMPTY FILE:", validate_csv(""))
    con = sqlite3.connect(":memory:")
    con.execute("CREATE TABLE aq(station TEXT, day TEXT, pm25 REAL)")
    readings = [("Adyar","2026-10-01",48.0),("Guindy","2026-10-01",95.0),("Guindy","2026-10-03",121.0),("Adyar","2026-10-04",60.0)]
    con.executemany("INSERT INTO aq VALUES (?,?,?)", readings)
    con.commit()
    def station_average(name):
        row = con.execute("SELECT AVG(pm25) FROM aq WHERE station = ?",(name,)).fetchone()
        return None if row[0] is None else round(row[0],1)
    print("AVERAGES:", station_average("Adyar"), station_average("Guindy"))
    print("INJECTION ATTEMPT:", station_average("Adyar' OR '1'='1"))
    # Unsafe string construction is shown for demonstration only; do not use in applications.
    payload = "Adyar' OR '1'='1"
    unsafe = "SELECT AVG(pm25) FROM aq WHERE station = '" + payload + "'"
    print("UNSAFE QUERY TEXT:", unsafe)
    print("SAFE QUERY RESULT:", station_average(payload))
    con.close()

if __name__ == "__main__": main()
