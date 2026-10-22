"""Task 1: Data model and validation rules for milk payment entries."""
from dataclasses import dataclass
from decimal import Decimal

@dataclass
class MilkEntry:
    farmer_id: str
    litres: Decimal
    fat: Decimal
    snf: Decimal
    shift: str

def validate_entry(entry):
    """Return True when the entry satisfies the assignment's basic rules."""
    if not entry.farmer_id.strip():
        raise ValueError("Farmer ID cannot be empty")
    if entry.litres <= 0:
        raise ValueError("Litres must be positive")
    if not Decimal("2.0") <= entry.fat <= Decimal("7.0"):
        raise ValueError("Fat must be between 2.0 and 7.0")
    if not Decimal("0") <= entry.snf <= Decimal("20"):
        raise ValueError("SNF must be between 0 and 20 (provisional assumption)")
    if entry.shift not in {"M", "E"}:
        raise ValueError("Shift must be M or E")
    return True

if __name__ == "__main__":
    example = MilkEntry("F001", Decimal("10.0"), Decimal("3.5"), Decimal("8.5"), "M")
    print("Entry:", example)
    print("Valid:", validate_entry(example))
