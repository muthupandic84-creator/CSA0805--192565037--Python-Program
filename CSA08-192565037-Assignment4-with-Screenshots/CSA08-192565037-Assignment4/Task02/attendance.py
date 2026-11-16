from pathlib import Path
from collections import defaultdict
import csv

def process_month(folder, output_folder):
    folder = Path(folder)
    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)
    counts = defaultdict(lambda: {"P": 0, "A": 0})
    errors = []

    for path in sorted(folder.glob("*.csv")):
        try:
            with path.open("r", encoding="utf-8", newline="") as source:
                for line_no, raw in enumerate(source, start=1):
                    fields = raw.strip().split(",")
                    if len(fields) != 3:
                        errors.append((path.name, line_no, raw.rstrip(), "expected 3 fields"))
                        continue
                    reg, date, status = [x.strip() for x in fields]
                    if not reg or not date or status not in {"P", "A"}:
                        errors.append((path.name, line_no, raw.rstrip(), "invalid field or status"))
                        continue
                    counts[reg][status] += 1
        except (OSError, UnicodeDecodeError) as exc:
            errors.append((path.name, 0, "", str(exc)))

    with (output_folder / "attendance_percentage.csv").open("w", encoding="utf-8", newline="") as out:
        writer = csv.writer(out)
        writer.writerow(["register_number", "present", "absent", "percentage"])
        for reg, c in sorted(counts.items()):
            total = c["P"] + c["A"]
            pct = (c["P"] / total * 100) if total else 0
            writer.writerow([reg, c["P"], c["A"], f"{pct:.2f}"])
    with (output_folder / "below_75.csv").open("w", encoding="utf-8", newline="") as out:
        writer = csv.writer(out)
        writer.writerow(["register_number", "attendance_percentage"])
        for reg, c in sorted(counts.items()):
            total = c["P"] + c["A"]
            pct = c["P"] / total * 100 if total else 0
            if pct < 75:
                writer.writerow([reg, f"{pct:.2f}"])
    with (output_folder / "damaged_lines.csv").open("w", encoding="utf-8", newline="") as out:
        writer = csv.writer(out)
        writer.writerow(["file_name", "line_number", "raw_line", "reason"])
        writer.writerows(errors)
    return counts, errors

if __name__ == "__main__":
    process_month(Path(__file__).parent, Path(__file__).parent / "output")
    print("Monthly attendance reports created.")
