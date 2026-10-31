"""Q3: Vehicle registration normalisation without regular expressions."""

def normalise(text):
    """Remove spaces/hyphens and uppercase the registration."""
    return text.strip().replace(" ", "").replace("-", "").upper()

def is_valid(reg):
    """Format: 2 letters, 2 digits, 1–2 letters, 4 digits."""
    if len(reg) not in (9, 10):
        return False
    if not reg[0:2].isalpha():
        return False
    if not reg[2:4].isdigit():
        return False
    series_length = len(reg) - 8
    if not reg[4:4 + series_length].isalpha():
        return False
    if not reg[-4:].isdigit():
        return False
    return True

def receipt_format(reg):
    if not is_valid(reg):
        raise ValueError("Cannot format an invalid registration number")
    return f"{reg[:2]} {reg[2:4]} {reg[4:-4]} {reg[-4:]}"

def main():
    samples = [
        "tn 09 ab 1234",
        "KA-01-M-0007",
        "TN9AB1234",
        "TN 22 1234 AB",
        "mh 12 xyz 6789",
        "DL-8C-1234",
    ]
    print(f"{'Input':20} {'Normalised':12} {'Result':8} Receipt")
    for raw in samples:
        reg = normalise(raw)
        valid = is_valid(reg)
        receipt = receipt_format(reg) if valid else "-"
        print(f"{raw:20} {reg:12} {'valid' if valid else 'INVALID':8} {receipt}")

    print("\nSlice inquiry:")
    for value in ("TN09AB1234", "TN09A1234"):
        print(value, "length =", len(value), "last four =", value[-4:],
              "middle =", value[4:-4])
    print("\nStrings are immutable: upper() returns a new string; it does not alter the original.")

if __name__ == "__main__":
    main()
