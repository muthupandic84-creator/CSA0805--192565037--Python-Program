from decimal import Decimal

# 1,000 payments of Rs 33.40 and three small adjustments of Rs 0.10
payments = ["33.40"] * 1000 + ["0.10"] * 3

def total_float(items):
    """Add amounts using binary floating-point."""
    total = 0.0
    for amount in items:
        total += float(amount)
    return total

def total_decimal(items):
    """Add decimal strings exactly using Decimal."""
    total = Decimal("0.00")
    for amount in items:
        total += Decimal(amount)
    return total

if __name__ == "__main__":
    print("float  :", total_float(payments))
    print("Decimal:", total_decimal(payments))
    print(0.1 + 0.2 == 0.3, Decimal("0.1") + Decimal("0.2") == Decimal("0.3"))
    print("Decimal(float('0.1')):", Decimal(float("0.1")))
