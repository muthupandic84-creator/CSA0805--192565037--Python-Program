from decimal import Decimal, InvalidOperation
from pathlib import Path

def total_mess_bills(filename):
    total = Decimal("0.00")
    report_rows = []
    rejected = []

    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line_number, raw_line in enumerate(file, start=1):
                line = raw_line.strip()
                if not line:
                    continue
                parts = [part.strip() for part in line.split(",")]
                if len(parts) != 3:
                    rejected.append((line_number, raw_line.rstrip("\n"), "expected 3 fields"))
                    continue
                register_no, name, amount_text = parts
                try:
                    amount = Decimal(amount_text)
                except InvalidOperation:
                    rejected.append((line_number, raw_line.rstrip("\n"), "amount is not numeric"))
                    continue
                if not amount.is_finite() or amount < 0:
                    rejected.append((line_number, raw_line.rstrip("\n"), "amount must be finite and non-negative"))
                    continue
                total += amount
                report_rows.append(f"{name}: {amount:.2f}")
    except (FileNotFoundError, PermissionError, UnicodeDecodeError) as exc:
        print(f"Could not process {filename}: {exc}")
        return

    print("\n".join(report_rows))
    print(f"Total {total:.2f}")
    print("Rejected lines:")
    for item in rejected:
        print(item)

if __name__ == "__main__":
    total_mess_bills(Path(__file__).with_name("mess_oct.txt"))
