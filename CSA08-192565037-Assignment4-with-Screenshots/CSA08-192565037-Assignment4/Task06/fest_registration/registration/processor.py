from pathlib import Path
import csv
from .reader import read_department_file
from .validator import validate_record, InvalidRegistration

def process_files(input_dir, output_dir, expected_departments=None):
    input_dir, output_dir = Path(input_dir), Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    expected_departments = expected_departments or []
    files = sorted(input_dir.glob("*.txt"))
    seen = set()
    master = []
    errors = []
    event_map = {}

    for department_file in files:
        try:
            for line_no, raw in read_department_file(department_file):
                if not raw.strip():
                    continue
                try:
                    record = validate_record(raw)
                    reg = record["register_number"]
                    if reg in seen:
                        raise InvalidRegistration(f"duplicate register number {reg}")
                    seen.add(reg)
                    master.append(record)
                    for event in record["events"]:
                        event_map.setdefault(event, []).append(record)
                except InvalidRegistration as exc:
                    errors.append((department_file.name, line_no, raw, str(exc)))
        except (FileNotFoundError, PermissionError, UnicodeDecodeError, OSError) as exc:
            errors.append((department_file.name, 0, "", f"{type(exc).__name__}: {exc}"))

    found_names = {p.name for p in files}
    for missing in expected_departments:
        if missing not in found_names:
            errors.append((missing, 0, "", "department file is missing"))

    with (output_dir / "master_list.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["register_number", "name", "department", "email", "events"])
        for r in master:
            writer.writerow([r["register_number"], r["name"], r["department"], r["email"], ";".join(r["events"])])

    for event, participants in event_map.items():
        safe_name = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in event)
        with (output_dir / f"event_{safe_name}.csv").open("w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["register_number", "name", "department", "email"])
            for r in participants:
                writer.writerow([r["register_number"], r["name"], r["department"], r["email"]])

    with (output_dir / "summary.txt").open("w", encoding="utf-8") as f:
        f.write(f"Valid unique registrations: {len(master)}\n")
        f.write(f"Events: {len(event_map)}\n")
        for event, participants in sorted(event_map.items()):
            f.write(f"{event}: {len(participants)} participants\n")

    with (output_dir / "error_log.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["file_name", "line_number", "raw_line", "reason"])
        writer.writerows(errors)

    return master, errors
