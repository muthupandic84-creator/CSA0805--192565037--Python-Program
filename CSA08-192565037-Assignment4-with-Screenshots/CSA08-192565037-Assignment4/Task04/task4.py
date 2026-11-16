from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent
LOG = ROOT / "returns.log"
ERROR_LOG = ROOT / "errors.log"

def save_returns(books):
    with LOG.open("a", encoding="utf-8") as log:
        for book in books:
            if book.strip():
                log.write(book.rstrip("\n") + "\n")

def process(day_file):
    try:
        with open(day_file, "r", encoding="utf-8") as source:
            books = source.readlines()
        save_returns(books)
    except (FileNotFoundError, PermissionError, UnicodeDecodeError, OSError) as exc:
        with ERROR_LOG.open("a", encoding="utf-8") as error_file:
            error_file.write(f"{datetime.now().isoformat()} | {day_file} | {type(exc).__name__}: {exc}\n")

if __name__ == "__main__":
    LOG.write_text("", encoding="utf-8")
    for name in ("day1.txt", "day2.txt", "day3.txt"):
        process(ROOT / name)
    print(LOG.read_text(encoding="utf-8"))
