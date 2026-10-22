def read_number(prompt):
    """Read a number, retrying until the user enters a valid decimal value."""
    while True:
        text = input(prompt).strip()
        try:
            # Decimal point is expected; values like '8,5' are rejected.
            return float(text)
        except ValueError:
            print("Invalid number. Enter a value such as 8.5.")

if __name__ == "__main__":
    litres = read_number("Enter litres: ")
    print(f"Quantity entered: {litres:8.2f} L")
