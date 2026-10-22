"""Validated milk payment calculator."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'Task07'))

from decimal import Decimal
from milkrate import payout, rate_per_litre

MIN_FAT = Decimal("2.0")
MAX_FAT = Decimal("7.0")
MIN_LITRES = Decimal("0")

def validate_entry(farmer_id, litres, fat, snf, shift):
    """Validate a farmer entry; raise ValueError if a rule is violated."""
    if not str(farmer_id).strip():
        raise ValueError("Farmer ID cannot be empty")
    litres, fat, snf = Decimal(str(litres)), Decimal(str(fat)), Decimal(str(snf))
    if litres <= MIN_LITRES:
        raise ValueError("Litres must be greater than zero")
    if not MIN_FAT <= fat <= MAX_FAT:
        raise ValueError("Fat must be between 2.0% and 7.0%")
    if not Decimal("0") <= snf <= Decimal("20"):
        raise ValueError("SNF must be between 0% and 20% (assumption; confirm local analyser limits)")
    if shift not in {"M", "E"}:
        raise ValueError("Shift must be M or E")
    return litres, fat, snf

def calculate_entry(farmer_id, litres, fat, snf, shift):
    """Validate one entry and return a result dictionary."""
    litres, fat, snf = validate_entry(farmer_id, litres, fat, snf, shift)
    rate = rate_per_litre(fat, snf)
    amount = payout(litres, fat, snf)
    return {"farmer_id": str(farmer_id), "shift": shift, "litres": litres,
            "fat": fat, "snf": snf, "rate": rate, "amount": amount}

def run_tests():
    """Run automated assertions for normal, boundary and invalid cases."""
    assert payout(10, 3.5, 8.5) == Decimal("300.00")
    assert payout(8.5, 4.2, 8.7) == Decimal("283.90")
    assert payout(12, 3.1, 8.3) == Decimal("333.60")
    assert rate_per_litre(2.0, 8.5) == Decimal("24.00")
    assert rate_per_litre(7.0, 8.5) == Decimal("44.00")
    for args in [("F1", -1, 3.5, 8.5, "M"), ("F2", 1, 7.1, 8.5, "E"), ("F3", "eight", 3.5, 8.5, "M")]:
        try:
            calculate_entry(*args)
        except (ValueError, ArithmeticError):
            pass
        else:
            raise AssertionError(f"Invalid entry unexpectedly accepted: {args}")
    print("All automated tests passed.")

if __name__ == "__main__":
    run_tests()
    print(calculate_entry("F001", 10, 3.5, 8.5, "M"))
