from pathlib import Path

def read_department_file(path):
    """Yield (line_number, raw_line); file-level errors are handled by caller."""
    with Path(path).open("r", encoding="utf-8") as source:
        for line_no, line in enumerate(source, start=1):
            yield line_no, line.rstrip("\n")
