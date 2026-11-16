import os
import tempfile

class InvalidRecord(Exception):
    """Raised when an attendance line is not in the expected format."""

def parse_line(line):
    parts = line.strip().split(",")
    if len(parts) != 3:
        raise InvalidRecord(f"expected 3 fields, found {len(parts)}")
    reg, date, status = (part.strip() for part in parts)
    if status not in {"P", "A"}:
        raise InvalidRecord(f"invalid status {status!r}")
    return reg, date, status

def summarise(path):
    present, absent, errors = 0, 0, []
    try:
        with open(path, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                if not line.strip():
                    continue
                try:
                    _, _, status = parse_line(line)
                except InvalidRecord as exc:
                    errors.append((line_number, str(exc)))
                    continue
                else:
                    if status == "P":
                        present += 1
                    else:
                        absent += 1
    except FileNotFoundError as exc:
        raise RuntimeError(f"attendance file not found: {path}") from exc
    except (PermissionError, UnicodeDecodeError, OSError) as exc:
        raise RuntimeError(f"could not read attendance file: {path}") from exc
    finally:
        # The with statement closes the file on success and on failure.
        pass
    return present, absent, errors

if __name__ == "__main__":
    data = ("192311001,2026-10-08,P\n192311002,2026-10-08,A\n"
            "192311003,2026-10-08\n192311004,2026-10-08,L\n")
    with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8") as tmp:
        tmp.write(data)
        name = tmp.name
    try:
        print(summarise(name))
    finally:
        os.remove(name)
